# -*- coding: UTF-8 -*-
from __future__ import unicode_literals

from datetime import datetime, timedelta
from django.contrib.contenttypes.models import ContentType
from serializers import (
    ScrapeJobSerializer,
    ScrapeJobListSerializer,
    ScrapeJobDetailListSerializer
)
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import (
    TokenAuthentication,
    SessionAuthentication
)
from management.apis.permissions import ApiAccessPermission
from scraping.models import ScrapeJob
from security.models import AuditLog, ACTION

__author__ = "axu"

"""
# 参考文档：
- [Django REST Framswork](http://www.django-rest-framework.org/)R
- [ModelViewSet](http://www.django-rest-framework.org/api-guide/viewsets/#modelviewset)
- [APIView](http://www.django-rest-framework.org/api-guide/views/#class-based-views)
"""


class ScrapeJobViewSet(viewsets.ModelViewSet):
    """数据采集任务接口"""
    # serializer_class = ScrapeJobSerializer
    queryset = ScrapeJob.objects.all()
    authentication_classes = (SessionAuthentication, TokenAuthentication, )
    permission_classes = (IsAuthenticated, ApiAccessPermission, )

    def get_serializer_class(self):
        if self.request.method == "GET":
            return ScrapeJobListSerializer
        else:
            return ScrapeJobSerializer

    def perform_create(self, serializer):
        # 创建
        interval = int(serializer.validated_data.get("interval"))
        next_time = datetime.now() + timedelta(seconds=interval)
        serializer.save(next_time=next_time)

        # 记录审计日志
        AuditLog.objects.create(
            user=self.request.user,
            content_type=ContentType.objects.get(model="scrapejob"),
            action=ACTION.CREATE,
            content=serializer.data
        )

    def perform_update(self, serializer):
        # 更新
        super(ScrapeJobViewSet, self).perform_update(serializer)
        # 记录审计日志
        AuditLog.objects.create(
            user=self.request.user,
            content_type=ContentType.objects.get(model="scrapejob"),
            action=ACTION.UPDATE,
            content=serializer.data
        )


class ScrapeJobDetailViewSet(viewsets.ReadOnlyModelViewSet):
    """数据采集任务详情接口"""

    serializer_class = ScrapeJobDetailListSerializer
    queryset = ScrapeJob.objects.all()
    authentication_classes = (SessionAuthentication, TokenAuthentication, )
    permission_classes = (IsAuthenticated, ApiAccessPermission, )
