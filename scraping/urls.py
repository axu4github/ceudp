# -*- coding: UTF-8 -*-
from django.conf.urls import url
from scraping import views

urlpatterns = [
    # /scraping/flat/
    url(r"flat/$", views.flat, name="flat"),
    # /scraping/create_scraping_task/
    url(r"create_scraping_task/$", views.create_scraping_task, name="create_scraping_task"),
]
