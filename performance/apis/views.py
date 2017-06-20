# -*- coding: UTF-8 -*-
from rest_framework import viewsets, mixins
from serializers import QuerySerializer
from performance.models import Query


class QueryViewSet(mixins.CreateModelMixin,
                   mixins.ListModelMixin,
                   mixins.RetrieveModelMixin,
                   viewsets.GenericViewSet):

    serializer_class = QuerySerializer
    queryset = Query.objects.all()

    def get_queryset(self):
        return Query.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.is_valid(raise_exception=True)
        excuted_query = serializer.validated_data.get("query")
        serializer.save(excuted_query=excuted_query, user=self.request.user)

    def list(self, request):
        reponses = super(QueryViewSet, self).list(request)
        return reponses
