# -*- coding: UTF-8 -*-
from __future__ import unicode_literals

from rest_framework import permissions
from django.core.urlresolvers import resolve

__author__ = "axu"


class ApiAccessPermission(permissions.BasePermission):
    """自定义权限"""

    def api_unique(self, request):
        """获取接口唯一标识"""
        unique = "{app}.{http_method}:{view_name}".format(
            app="management",
            http_method=request.method,
            view_name=resolve(request.path).view_name)
        return unique.lower()

    def has_permission(self, request, view):
        """判断用户是否有接口权限"""
        # return request.user.has_perm(self.api_unique(request))
        return True
