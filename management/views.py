# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.contenttypes.models import ContentType
from management.authentications import Authentication
from security.models import AuditLog, ACTION

__author__ = "axu"


def login(request):
    if request.method == "POST":
        if "username" in request.POST and "password" in request.POST:
            try:
                username = request.POST["username"]
                password = request.POST["password"]
                user = Authentication.authenticate(username, password)
                auth_login(request, user)  # 系统登陆
                user.get_or_create_token()  # 获得用户Token

                AuditLog.objects.create(
                    user=user,
                    content_type=ContentType.objects.get(model="user"),
                    action=ACTION.LOGIN
                )

                return HttpResponseRedirect(reverse("index"))
            except Exception as e:
                return render(request, "ceudp/login.html", {"error_messages": str(e)})

    return render(request, "ceudp/login.html")


def logout(request):

    # AuditLog.objects.create(
    #     user=request.user,
    #     content_type=ContentType.objects.get(model="user"),
    #     action=ACTION.LOGOUT
    # )

    auth_logout(request)  # 系统登出

    return HttpResponseRedirect(reverse("management:login"))


def users(request):
    """用户管理页面"""
    return render(request, "management/users.html")


def groups(request):
    """用户管理页面"""
    return render(request, "management/groups.html")
