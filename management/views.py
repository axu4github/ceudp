# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.translation import ugettext as _


def login(request):
    if request.method == "POST":
        if "username" in request.POST and "password" in request.POST:
            username = request.POST["username"]
            password = request.POST["password"]
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    auth_login(request, user)  # 系统登陆
                    user.get_or_create_token() # 获得用户Token
                    return HttpResponseRedirect(reverse("index"))
                else:
                    return render(request, "ceudp/login.html", {"error_messages": _("user has been disabled.")})
            else:
                return render(request, "ceudp/login.html", {"error_messages": _("username or password were incorrect.")})
        else:
            return render(request, "ceudp/login.html", {"error_messages": "none username or passoword."})

    return render(request, "ceudp/login.html")


def logout(request):
    auth_logout(request)  # 系统登出
    return HttpResponseRedirect(reverse("management:login"))
