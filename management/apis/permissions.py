# -*- coding: UTF-8 -*-
from __future__ import unicode_literals

from rest_framework import permissions
from django.core.urlresolvers import resolve
from ceudp.utilities.loggables import Loggable

__author__ = "axu"


class ApiAccessPermission(permissions.BasePermission, Loggable):
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
        user = request.user
        permission_str = self.api_unique(request)
        # self.log_info("用户: {0}".format(user.username))
        # self.log_info("权限: {0}".format(permission_str))
        return user.has_perm(permission_str)
