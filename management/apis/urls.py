# -*- coding: UTF-8 -*-

__author__ = "axu"

from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from views import MenuViewSet

# 参考文档：http://www.django-rest-framework.org/api-guide/routers/
# Example:
# - URL pattern: ^users/$ Name: 'user-list'
# - URL pattern: ^users/{pk}/$ Name: 'user-detail'
# - URL pattern: ^accounts/$ Name: 'account-list'
# - URL pattern: ^accounts/{pk}/$ Name: 'account-detail'
router = DefaultRouter()
router.register(r"menus", MenuViewSet)

urlpatterns = [
    url(r"^", include(router.urls)),
]
