# -*- coding: UTF-8 -*-
from django.conf.urls import url, include
from views import QueryViewSet
from rest_framework.routers import DefaultRouter

# 参考文档：http://www.django-rest-framework.org/api-guide/routers/
# Example:
# - URL pattern: ^users/$ Name: 'user-list'
# - URL pattern: ^users/{pk}/$ Name: 'user-detail'
# - URL pattern: ^accounts/$ Name: 'account-list'
# - URL pattern: ^accounts/{pk}/$ Name: 'account-detail'
router = DefaultRouter()
router.register(r"querys", QueryViewSet)

urlpatterns = [
    url(r"^", include(router.urls)),
]
