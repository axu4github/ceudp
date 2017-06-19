# -*- coding: UTF-8 -*-
from rest_framework import serializers
from performance.models import Query


class QuerySerializer(serializers.ModelSerializer):

    class Meta:
        model = Query
        fields = "__all__"
