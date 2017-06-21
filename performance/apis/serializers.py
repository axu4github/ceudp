# -*- coding: UTF-8 -*-
from rest_framework import serializers
from performance.models import Query


class QuerySerializer(serializers.ModelSerializer):

    def validate_query(self, query):

        sql = query.lower()
        if not sql.startswith("select"):
            raise serializers.ValidationError("只允许输入`SELECT`语句.")

    class Meta:
        model = Query
        fields = "__all__"
