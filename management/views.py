# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse


def login(request):
    if request.method == "POST":
        if "username" in request.POST and "password" in request.POST:
            user = authenticate(
                request.POST["username"], request.POST["password"])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(reverse("index"))
                else:
                    return render(request, "ceudp/login.html", {error_messages: ""})
            else:
                return render(request, "ceudp/login.html", {error_messages: ""})
        else:
            return render(request, "ceudp/login.html", {error_messages: ""})

    return render(request, "ceudp/login.html")
