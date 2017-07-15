# -*- coding: UTF-8 -*-
from __future__ import unicode_literals

from serializers import (
    AuditLogSerializer
)
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import (
    TokenAuthentication,
    SessionAuthentication
)
from management.apis.permissions import ApiAccessPermission
from security.models import AuditLog

__author__ = "axu"


class AuditLogViewSet(viewsets.ReadOnlyModelViewSet):
    """权限接口"""
    serializer_class = AuditLogSerializer
    queryset = AuditLog.objects.all()
    authentication_classes = (SessionAuthentication, TokenAuthentication, )
    permission_classes = (IsAuthenticated, ApiAccessPermission, )
