# -*- coding: UTF-8 -*-
from django.conf.urls import url, include
from views import QueryViewSet, UnstructuredDataViewSet
from rest_framework.routers import DefaultRouter
# from django.views.decorators.csrf import csrf_exempt

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
    url(r'unstructured_datas/$',
        UnstructuredDataViewSet.as_view(
            {'post': 'create', 'get': 'list', 'delete': 'destroy'}),
        name='unstructured_datas'),
    url(r'unstructured_datas/search/$',
        UnstructuredDataViewSet.as_view({'get': 'search'}),
        name='unstructured_search'),
]
