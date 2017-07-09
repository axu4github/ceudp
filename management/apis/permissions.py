# -*- coding: UTF-8 -*-
from __future__ import unicode_literals

from rest_framework import permissions
from django.core.urlresolvers import resolve

__author__ = "axu"


class ApiAccessPermission(permissions.BasePermission):
    """自定义权限"""

    def api_unique(self, request):
        """获取接口唯一标识"""
        unique = "{http_method}:{view_name}".format(
            http_method=request.method,
            view_name=resolve(request.path).view_name)
        return unique.lower()

    def has_permission(self, request, view):
        # print self.api_unique(request)
        return True
