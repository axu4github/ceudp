# -*- coding: UTF-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from views import (
    ScrapeJobViewSet,
    ScrapeJobDetailViewSet
)

__author__ = "axu"

"""
Router参考文档：http://www.django-rest-framework.org/api-guide/routers/

Example:
- URL pattern: ^users/$ Name: 'user-list'
- URL pattern: ^users/{pk}/$ Name: 'user-detail'
- URL pattern: ^accounts/$ Name: 'account-list'
- URL pattern: ^accounts/{pk}/$ Name: 'account-detail'

ClassBasedViews参考文档：http://www.django-rest-framework.org/api-guide/views/#class-based-views
"""

router = DefaultRouter()
router.register(r"scrapejobs", ScrapeJobViewSet)
router.register(r"scrapejobdetails", ScrapeJobDetailViewSet)

urlpatterns = [
    url(r"^", include(router.urls)),
]
