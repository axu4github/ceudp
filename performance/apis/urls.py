# -*- coding: UTF-8 -*-
from django.conf.urls import url, include
from views import QueryViewSet
from rest_framework.routers import DefaultRouter

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'querys', QueryViewSet)


urlpatterns = [
    url(r"^", include(router.urls)),
]
