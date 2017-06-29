# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

def flat(request):
    return render(request, "scraping/flat.html")

def create_scraping_task(request):
    return render(request, "scraping/create_scraping_task.html")
