# -*- coding: UTF-8 -*-
from rest_framework import viewsets, mixins, status
from serializers import QuerySerializer
from performance.models import Query
from rest_framework.response import Response
from ceudp.utilities.loggables import Loggable
from performance.settings import settings
from collections import OrderedDict

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

    def get_queryset(self):
        return Query.objects.filter(user=self.request.user)

    def create(self, request):
        """执行查询接口"""
        response_context = OrderedDict()
        self.log_debug(
            "request datas: [{request_data}]".format(request_data=request.data))
        response_context["request_set"] = request.data
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)  # 校验请求参数
        new_query = serializer.save(user=self.request.user)
        response_context["response_set"] = {"id": new_query.id}
        try:
            query_results = new_query.execute()
            new_query.executed_query = query_results["executed_query"]
            new_query.duration = query_results["duration"]
            new_query.rows = query_results["total"]
            new_query.status = settings.SUCCESS
            new_query.save()
            response_context["response_set"].update(query_results)
            response_context["status"] = settings.SUCCESS
            response = Response(response_context, status.HTTP_200_OK)
        except Exception as e:
            new_query.status = settings.FAILED
            new_query.error_messages = str(e)
            new_query.save()
            response_context["status"] = settings.FAILED
            response_context["error_message"] = str(e)
            response = Response(response_context, status.HTTP_400_BAD_REQUEST)

        return response

    def list(self, request):
        """获取历史查询记录的接口"""
        reponses = super(QueryViewSet, self).list(request)
        return reponses
