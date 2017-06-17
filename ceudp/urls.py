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

urlpatterns = [
    # /
    url(r"^$", login_required(dashboard_views.index), name="index"),
    # /login
    url(r"^login/$", login, name="login"),
    # /logout
    url(r"^logout/$", logout, name="logout"),
    # /admin/
    url(r"^admin/", admin.site.urls),
    # /dashboard/
    url(r"^dashboard/", include("dashboard.urls")),
    # /performance/
    url(r"^performance/", include("performance.urls", namespace="performance")),
    # /management/
    url(r"^management/", include("management.urls", namespace="management")),
]
