# -*- coding: UTF-8 -*-
from django.conf.urls import url
from views import QueryViewSet


urlpatterns = [
    url(r"querys/$", QueryViewSet.as_view({'get': 'list'}), name="query_list"),
]
