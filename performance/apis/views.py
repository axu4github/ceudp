# -*- coding: UTF-8 -*-
from rest_framework import viewsets, mixins
from serializers import QuerySerializer
from performance.models import Query
from rest_framework.response import Response
from ceudp.utilities.loggables import Loggable


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
        response = []
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)  # 校验请求参数
            query = serializer.validated_data.get("query")
            # results = Query.objects.run(query, **serializer.validated_data)
            # serializer.save()
            # response.append(serializer.validated_data)
            self.log_debug(serializer.validated_data)
        except Exception as e:
            raise

        return Response(response)

    def list(self, request):
        reponses = super(QueryViewSet, self).list(request)
        return reponses
