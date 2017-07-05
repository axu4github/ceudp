# -*- coding: UTF-8 -*-
from __future__ import unicode_literals

from rest_framework import permissions
from django.core.urlresolvers import resolve

__author__ = "axu"


class CustomerAccessPermission(permissions.BasePermission):
    """自定义权限"""

    def api_unique(self, request):
        """获取接口唯一标识"""
        return "{http_method}:{view_name}".format(
            http_method=request.method.lower(),
            view_name=resolve(request.path).view_name)

    def has_permission(self, request, view):
        # print self.api_unique(request)
        return True
