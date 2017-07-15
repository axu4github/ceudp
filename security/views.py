# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

__author__ = "axu"


def auditlog(request):
    """用户管理页面"""
    return render(request, "security/auditlog.html")
