# -*- coding: UTF-8 -*-
from django.conf.urls import url
from performance import views

app_name = "performance"

urlpatterns = [
    # /performance/filesystem/
    url(r"filesystem/$", views.filesystem, name="filesystem"),
]
