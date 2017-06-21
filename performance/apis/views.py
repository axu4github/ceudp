# -*- coding: UTF-8 -*-
from rest_framework import viewsets, mixins
from serializers import QuerySerializer
from performance.models import Query
from rest_framework.response import Response
from ceudp.utilities.loggables import Loggable
from performance.settings import settings

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
        self.log_debug(
            "request datas: [{request_data}]".format(request_data=request.data))
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)  # 校验请求参数
        new_query = serializer.save(user=self.request.user)
        try:
            query_results = new_query.execute()
            # new_query.save(
            #     executed_query=query_results["executed_query"],
            #     duration=query_results["duration"],
            #     rows=query_results["rows"],
            #     status=settings.QUERY_STASTUS[settings.SUCCESS],
            # )
        except Exception as e:
            raise e
            # new_query.save(
            #     status=settings.QUERY_STASTUS[settings.FAILED], error_messages=e)

        return Response(query_results)

    def list(self, request):
        """获取历史查询记录的接口"""
        reponses = super(QueryViewSet, self).list(request)
        return reponses
