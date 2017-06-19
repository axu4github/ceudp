# -*- coding: UTF-8 -*-
from django.conf.urls import url
from performance import views

urlpatterns = [
    # /performance/filesystem/
    url(r"fs/$", views.filesystem, name="filesystem"),
    # /performance/filesystem/
    url(r"sql/$", views.sql_lab, name="sql_lab"),
]
