# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse


def login(request):
    if request.method == "POST":
        if "username" in request.POST and "password" in request.POST:
            username = request.POST["username"]
            password = request.POST["password"]
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    auth_login(request, user)  # 系统登陆
                    return HttpResponseRedirect(reverse("index"))
                else:
                    return render(request, "ceudp/login.html", {error_messages: ""})
            else:
                return render(request, "ceudp/login.html", {error_messages: ""})
        else:
            return render(request, "ceudp/login.html", {error_messages: ""})

    return render(request, "ceudp/login.html")


def logout(request):
    auth_logout(request)  # 系统登出
    return HttpResponseRedirect(reverse("management:login"))
