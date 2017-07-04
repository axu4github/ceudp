# -*- coding: UTF-8 -*-
from rest_framework import viewsets, mixins, status
from serializers import QuerySerializer
from performance.models import Query
from rest_framework.response import Response
from ceudp.utilities.loggables import Loggable
from performance.settings import settings
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated

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
    permission_classes = (IsAuthenticated, )

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
