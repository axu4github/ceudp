# -*- coding: UTF-8 -*-
from __future__ import unicode_literals

from rest_framework import viewsets, views
from serializers import MenuSerializer
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from management.models import Menu
from rest_framework.response import Response

__author__ = "axu"

"""
# 参考文档：
- [Django REST Framswork](http://www.django-rest-framework.org/)
- [ModelViewSet](http://www.django-rest-framework.org/api-guide/viewsets/#modelviewset)
- [APIView](http://www.django-rest-framework.org/api-guide/views/#class-based-views)
"""


class LoginViewSet(views.APIView):
    """用户登录接口（获取用户Token）"""

    authentication_classes = ()
    permission_classes = (AllowAny, )

    def post(self, request):
        username = request.data.get("username", None)
        password = request.data.get("password", None)
        return Response([username, password])


class MenuViewSet(viewsets.ModelViewSet):
    """菜单接口"""

    serializer_class = MenuSerializer
    queryset = Menu.objects.all()
    authentication_classes = (SessionAuthentication, TokenAuthentication, )
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        return self.request.user.menus.all()
