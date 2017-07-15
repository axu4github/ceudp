# -*- coding: UTF-8 -*-
from django.conf.urls import url
from views import auditlog

__author__ = "axu"

urlpatterns = [
    # /security/auditlog/
    url(r"^auditlog/", auditlog, name="auditlog"),
]
