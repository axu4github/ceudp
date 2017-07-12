# -*- coding: UTF-8 -*-

"""ceudp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from dashboard import views as dashboard_views
from management.views import login, logout
from django.contrib.auth.decorators import login_required
from rest_framework_swagger.views import get_swagger_view
from ceudp.apis import SwaggerSchemaView
schema_view = get_swagger_view(title='统一数据平台 API')

urlpatterns = [
    # /
    # url(r"^$", login_required(dashboard_views.index), name="index"),
    url(r"^$", dashboard_views.index, name="index"),
    # /apis
    url(r"^apis/$", login_required(schema_view), name="apis"),
    url(r'^api-doc/$', SwaggerSchemaView.as_view(), name='docs'),
    # /login
    url(r"^login/$", login, name="login"),
    # /logout
    url(r"^logout/$", logout, name="logout"),
    # /admin/
    url(r"^admin/", admin.site.urls),
    # /dashboard/
    url(r"^dashboard/", include("dashboard.urls")),
    # /performance/
    url(r"^performance/",
        include("performance.urls", namespace="performance")),
    # /api/performance/
    url(r"^api/performance/",
        include("performance.apis.urls", namespace="performance_api")),
    # /management/
    url(r"^management/", include("management.urls", namespace="management")),
    # /api/management/
    url(r"^api/management/",
        include("management.apis.urls", namespace="management_api")),
    # /scraping/
    url(r"^scraping/", include("scraping.urls", namespace="scraping")),
]
