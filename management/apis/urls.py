# -*- coding: UTF-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from views import (
    MenuViewSet,
    LoginViewSet,
    UserViewSet,
    GroupViewSet,
    PermissionViewSet,
    ColumnTypeViewSet,
    DatabaseViewSet
)

__author__ = "axu"

"""
Router参考文档：http://www.django-rest-framework.org/api-guide/routers/

Example:
- URL pattern: ^users/$ Name: 'user-list'
- URL pattern: ^users/{pk}/$ Name: 'user-detail'
- URL pattern: ^accounts/$ Name: 'account-list'
- URL pattern: ^accounts/{pk}/$ Name: 'account-detail'

ClassBasedViews参考文档：http://www.django-rest-framework.org/api-guide/views/#class-based-views
"""

router = DefaultRouter()
router.register(r"menus", MenuViewSet)
router.register(r"users", UserViewSet)
router.register(r"groups", GroupViewSet)
router.register(r"permissions", PermissionViewSet)
router.register(r"columntypes", ColumnTypeViewSet)
router.register(r"databases", DatabaseViewSet)

urlpatterns = [
    url(r"^", include(router.urls)),
    url(r"login/$", LoginViewSet.as_view(), name="login"),
]
