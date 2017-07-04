# -*- coding: UTF-8 -*-
from __future__ import unicode_literals

from rest_framework import viewsets, views, status
from serializers import MenuSerializer
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from management.models import Menu
from management.authentications import Authentication
from rest_framework.response import Response
from django.conf import settings

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
        try:
            username = request.data.get("username", None)
            password = request.data.get("password", None)
            user = Authentication.authenticate(username, password)
            token = user.get_or_create_token()  # 获得用户Token
            response_context = {
                "status": settings.SUCCESS,
                "token": token.key,
            }

            response = Response(response_context, status.HTTP_200_OK)
        except Exception as e:
            response_context = {
                "status": settings.FAILED,
                "message": str(e),
            }

            response = Response(response_context, status.HTTP_400_BAD_REQUEST)

        return response


class MenuViewSet(viewsets.ModelViewSet):
    """菜单接口"""

    serializer_class = MenuSerializer
    queryset = Menu.objects.all()
    authentication_classes = (SessionAuthentication, TokenAuthentication, )
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        return self.request.user.menus.all()
