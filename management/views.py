# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.contrib.auth import login as auth_login, logout as auth_logout
from management.authentications import Authentication
from django.http import HttpResponseRedirect
from django.urls import reverse

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
                return HttpResponseRedirect(reverse("index"))
            except Exception as e:
                return render(request, "ceudp/login.html", {"error_messages": str(e)})

    return render(request, "ceudp/login.html")


def logout(request):
    auth_logout(request)  # 系统登出
    return HttpResponseRedirect(reverse("management:login"))
