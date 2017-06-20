# -*- coding: UTF-8 -*-
from django.conf.urls import url, include
from views import QueryViewSet
from rest_framework.routers import DefaultRouter

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r"querys", QueryViewSet)


urlpatterns = [
    url(r"^", include(router.urls)),
    # POST /api/performance/querys/
    # url(r"^querys/$", QueryViewSet.as_view({"post": "create"}), name="query_create"),
    # # GET /api/performance/querys/
    # url(r"^querys/$", QueryViewSet.as_view({"get": "list", "post": "create"}), name="query"),
    # # GET /api/performance/querys/1/
    # url(r"^querys/(?P<pk>\d+)/$", QueryViewSet.as_view({"get": "retrieve"}), name="query_detail"),
]
