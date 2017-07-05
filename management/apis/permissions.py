# -*- coding: UTF-8 -*-
from __future__ import unicode_literals

from rest_framework import permissions

__author__ = "axu"


class CustomerAccessPermission(permissions.BasePermission):
    """自定义权限"""

    def has_permission(self, request, view):
        return True
