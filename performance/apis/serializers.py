# -*- coding: UTF-8 -*-
from rest_framework import serializers
from performance.models import Query


class QuerySerializer(serializers.ModelSerializer):

    def validate_query(self, query):
        query = query.lower()
        if not query.startswith("select"):
            raise serializers.ValidationError("只允许输入`SELECT`语句.")

        return query

    class Meta:
        model = Query
        fields = "__all__"
