# -*- coding: UTF-8 -*-
from rest_framework import serializers
from scraping.models import ScrapeJob

__author__ = "axu"

"""
参考文档：
- [ModelSerializer](http://www.django-rest-framework.org/api-guide/serializers/#modelserializer)
"""


class ScrapeJobSerializer(serializers.ModelSerializer):

    class Meta:
        model = ScrapeJob
        fields = ("id", "job_name", "job_type",
                  "data_source", "destination", "interval")


class ScrapeJobListSerializer(serializers.ModelSerializer):

    class Meta:
        model = ScrapeJob
        fields = "__all__"
