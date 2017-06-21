# -*- coding: UTF-8 -*-
from rest_framework import viewsets, mixins
from serializers import QuerySerializer
from performance.models import Query
from rest_framework.response import Response
from ceudp.utilities.loggables import Loggable
from performance.settings import settings


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
        self.log_debug("request datas: [{request_data}]".format(request_data=request.data))
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)  # 校验请求参数
        new_query = serializer.save(user=self.request.user)
        # try:
        #     query_results = new_query.execute()
        #     new_query.save(
        #         executed_query=query_results["executed_query"],
        #         duration=query_results["duration"],
        #         rows=query_results["rows"],
        #         status=settings.QUERY_STASTUS[settings.SUCCESS],
        #     )
        # except Exception as e:
        #     new_query.save(
        #         status=settings.QUERY_STASTUS[settings.FAILED], 
        #         error_messages=e
        #     )

        return Response(new_query.query)

    def list(self, request):
        reponses = super(QueryViewSet, self).list(request)
        return reponses
