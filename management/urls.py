# -*- coding: UTF-8 -*-
from django.conf.urls import url
from views import login, logout

urlpatterns = [
    # /management/login/
    url(r"^login/", login, name="login"),
    # /management/logout/
    url(r"^logout/", logout, name="logout"),
]
