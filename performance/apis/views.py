# -*- coding: UTF-8 -*-

import os
import tempfile
from django.http import StreamingHttpResponse
from serializers import QuerySerializer
from ceudp.utilities.loggables import Loggable
from management.apis.permissions import ApiAccessPermission
from performance.models import Query
from performance.hdfs_clients import HDFSClient
from performance.settings import settings
from performance.utils import Utils
from rest_framework import viewsets, mixins, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import (
    TokenAuthentication,
    SessionAuthentication
)


__author__ = "axu"

"""
# 参考文档：
- [Django REST Framswork](http://www.django-rest-framework.org/)
"""


class QueryViewSet(mixins.CreateModelMixin,
                   mixins.ListModelMixin,
                   mixins.RetrieveModelMixin,
                   viewsets.GenericViewSet,
                   Loggable):
    """查询接口"""

    serializer_class = QuerySerializer
    queryset = Query.objects.all()
    authentication_classes = (SessionAuthentication, TokenAuthentication, )
    permission_classes = (IsAuthenticated, ApiAccessPermission)

    def get_queryset(self):
        return Query.objects.filter(user=self.request.user)

    def create(self, request):
        """执行查询接口"""
        response_context = {}
        self.log_debug("Request Datas: [{r}]".format(r=request.data))
        response_context["request_set"] = request.data
        # 验证并记录请求信息
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)  # 校验请求参数
        new_query = serializer.save(user=self.request.user)
        # 获取查询id
        response_context["response_set"] = {"id": new_query.id}
        # 根据请求SQL进行查询
        try:
            # 执行查询
            query_results = new_query.execute()
            # 记录查询结果信息
            new_query.status = settings.SUCCESS
            new_query.executed_query = query_results["executed_query"]
            new_query.duration = query_results["duration"]
            new_query.rows = query_results["total"]
            new_query.save()
            # 生成响应信息
            response_context["status"] = settings.SUCCESS
            # 将查询结果写入响应信息中
            response_context["response_set"].update(query_results)
            response = Response(response_context, status.HTTP_200_OK)
        except Exception as e:
            # 记录失败信息
            new_query.status = settings.FAILED
            new_query.error_messages = str(e)
            new_query.save()
            # 生成响应信息
            response_context["status"] = settings.FAILED
            response_context["error_message"] = str(e)
            response = Response(response_context, status.HTTP_400_BAD_REQUEST)

        return response

    def list(self, request):
        """获取历史查询记录的接口"""
        query_set = map(lambda q: q.as_dict(),
                        Query.objects.filter(user=self.request.user))
        return Response(query_set)


class StreamingFileResponse(StreamingHttpResponse):
    """文件流下载"""

    def file_iterator(self, chunk_size=512):
        with open(self.filename) as f:
            while True:
                c = f.read(chunk_size)
                if c:
                    yield c
                else:
                    break

    def __init__(self, filename=None, **kwargs):
        if filename is None:
            raise Exception("StreamingFileResponse __init__ filename is none.")

        self.filename = filename
        # 设置返回内容类型为流
        kwargs.setdefault('content_type', 'application/octet-stream')

        # 不优美的实现
        # django kwarg中并没有预设content_disposition or content-disposition属性，而且在这里设置时会报错。
        # 具体信息可以详见官网针对response的说明：https://docs.djangoproject.com/en/dev/ref/request-response/
        #（There’s nothing Django-specific about the Content-Disposition header, but it’s easy to forget the syntax, so we’ve included it here.）
        #
        # import os
        # kwargs.setdefault(
        #     'content_disposition', 'attachment;filename="{0}"'.format(os.path.basename(self.filename)))

        super(StreamingFileResponse, self).__init__(
            self.file_iterator(), **kwargs)


class ResponseContext(object):
    """响应内容类"""

    def __init__(self, status=status.HTTP_200_OK,
                 message='', request_set=None, response_set=None):
        self.status = status
        self.message = message
        self.request_set = request_set
        self.response_set = response_set

    @property
    def data(self):
        response_context = {'status': self.status, 'message': self.message}
        if self.request_set is not None:
            response_context['request_set'] = self.request_set

        if self.response_set is not None:
            response_context['response_set'] = self.response_set

        return response_context


class UnstructuredDataViewSet(viewsets.ViewSet, Loggable):
    """非结构化数据方法集"""

    authentication_classes = ()
    permission_classes = ()

    def create(self, request):
        """非结构化数据上传接口"""
        try:
            hdfs_path = request.data['hdfs_path']
            local_path = request.data.get('local_path', None)

            upload_file = request.FILES.get('upload_file', None)
            hdfs_client = HDFSClient(settings.HDFS_WEB_URL)

            if upload_file is not None:
                upload_file_name = upload_file.name
                tmp_file = "{0}/{1}".format(
                    tempfile.mkdtemp(), upload_file_name)
                request.data.update({'tmp_file': tmp_file})
                # 从请求中删除，要不最后返回结果的时候会带着内容一起返回，导致返回请求内容过大
                del request.data['upload_file']
                Utils.file_put_contents(tmp_file, upload_file.read())
                local_path = tmp_file

            hdfs_client.upload(hdfs_path, local_path, overwrite=True)

            response_context = ResponseContext(status=status.HTTP_200_OK,
                                               message=settings.SUCCESS,
                                               request_set=request.data)
            response = Response(response_context.data, status.HTTP_200_OK)
        except Exception, e:
            response_context = ResponseContext(status=status.HTTP_400_BAD_REQUEST,
                                               message=str(e),
                                               request_set=request.data)
            response = Response(response_context.data,
                                status.HTTP_400_BAD_REQUEST)

        return response

    def list(self, request):
        """非结构化数据删除接口"""
        try:
            meta = request.GET.get('meta')
            self.log_debug("request.GET: {0}".format(request.GET))
            self.log_debug("meta: {0}".format(meta))
            if meta is not None and "FALSE" == str(meta).upper():
                meta = False
            else:
                meta = True

            hdfs_client = HDFSClient(settings.HDFS_WEB_URL)
            hdfs_path = request.GET.get('hdfs_path')

            self.log_debug(
                "Function list: (hdfs_path, meta): ({0}, {1})".format(hdfs_path, meta))

            if meta:
                response_set = hdfs_client.list(hdfs_path)
                response_context = ResponseContext(status=status.HTTP_200_OK,
                                                   message=settings.SUCCESS,
                                                   request_set={
                                                       'hdfs_path': request.GET.get('hdfs_path')},
                                                   response_set=response_set)

                response = Response(response_context.data, status.HTTP_200_OK)
            else:
                if not hdfs_client.is_file(hdfs_path):
                    raise Exception(
                        "Not Supported Dictionary: {0}".format(hdfs_path))

                (_, local_path) = tempfile.mkstemp()
                hdfs_client.download(hdfs_path, local_path)
                response = StreamingFileResponse(local_path)
                response['Content-Disposition'] = 'attachment;filename="{0}"'.format(
                    os.path.basename(hdfs_path))

        except Exception, e:
            response_context = ResponseContext(status=status.HTTP_400_BAD_REQUEST,
                                               message=str(e),
                                               request_set={'hdfs_path': request.GET.get('hdfs_path')})
            response = Response(response_context.data,
                                status.HTTP_400_BAD_REQUEST)

        return response

    def destroy(self, request):
        """非结构化数据删除接口"""

        try:
            hdfs_path = request.data['hdfs_path']
            hdfs_client = HDFSClient(settings.HDFS_WEB_URL)
            hdfs_client.delete(hdfs_path)
            response_context = ResponseContext(status=status.HTTP_200_OK,
                                               message=settings.SUCCESS,
                                               request_set={'hdfs_path': hdfs_path})

            response = Response(response_context.data, status.HTTP_200_OK)
        except Exception, e:
            response_context = ResponseContext(status=status.HTTP_400_BAD_REQUEST,
                                               message=str(e),
                                               request_set=request.data)
            response = Response(response_context.data,
                                status.HTTP_400_BAD_REQUEST)

        return response

    def search(self, request):
        """非结构化数据搜索接口"""
        contents = request.GET.get('contents')
        self.log_debug("contents: {0}".format(contents))
        try:
            hdfs_client = HDFSClient(settings.HDFS_WEB_URL)
            response_set = hdfs_client.search(contents)
            response_context = ResponseContext(status=status.HTTP_200_OK,
                                               message=settings.SUCCESS,
                                               request_set={
                                                   'contents': contents},
                                               response_set=response_set)
            response = Response(response_context.data, status.HTTP_200_OK)
        except Exception, e:
            response_context = ResponseContext(status=status.HTTP_400_BAD_REQUEST,
                                               message=str(e),
                                               request_set=request.data)
            response = Response(response_context.data,
                                status.HTTP_400_BAD_REQUEST)

        return response
