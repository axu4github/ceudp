# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.views import generic


def filesystem(request):
    return render(request, "performance/filesystem.html")


def sql_lab(request):
    return render(request, "performance/sql_lab.html")
