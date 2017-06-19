# -*- coding: UTF-8 -*-
from rest_framework import viewsets
from serializers import QuerySerializer
from performance.models import Query


class QueryViewSet(viewsets.ModelViewSet):
    serializer_class = QuerySerializer

    def get_queryset(self):
        return Query.objects.filter(user=self.request.user)
