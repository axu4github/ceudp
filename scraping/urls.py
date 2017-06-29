# -*- coding: UTF-8 -*-
from django.conf.urls import url
from scraping import views

urlpatterns = [
    # /scraping/flat/
    url(r"flat/$", views.flat, name="flat"),
]
