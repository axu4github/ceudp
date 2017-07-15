# -*- coding: UTF-8 -*-
from __future__ import unicode_literals

from itertools import chain
from django.contrib.auth.models import Permission, Group
from django.contrib.contenttypes.models import ContentType
from serializers import (
    MenuSerializer,
    UserSerializer,
    PasswordSerializer,
    GroupSerializer,
    PermissionSerializer
)
from rest_framework import viewsets, views, status, mixins
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from rest_framework.authentication import (
    TokenAuthentication,
    SessionAuthentication
)
from management.apis.permissions import ApiAccessPermission
from management.models import Menu, User
from management.authentications import Authentication
from management.settings import settings

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
    permission_classes = (IsAuthenticated, ApiAccessPermission, )


class UserViewSet(mixins.CreateModelMixin,
                  mixins.ListModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  viewsets.GenericViewSet):
    """
    用户接口

    因为不想提供DELETE方法，所以使用mixins完成自定义ModelViewSet

    参考文档：http://www.django-rest-framework.org/api-guide/viewsets/#custom-viewset-base-classes
    """

    serializer_class = UserSerializer
    queryset = User.objects.all()
    authentication_classes = (SessionAuthentication, TokenAuthentication, )
    permission_classes = (IsAuthenticated, ApiAccessPermission, )

    # def list(self, request):
    #     """用户列表"""
    #     queryset = User.objects.all()
    #     serializer = UserSerializer(queryset, many=True)
    #     return Response(serializer.data)

    @detail_route(methods=["post"])
    def change_password(self, request, pk=None):
        """修改密码"""
        try:
            serializer = PasswordSerializer(data=request.data)
            if serializer.is_valid():
                self.request.user.set_password(serializer.data["password"])
                self.request.user.save()
                response = Response({}, status=status.HTTP_200_OK)
            else:
                response = Response(
                    serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            response = Response(str(e), status=status.HTTP_400_BAD_REQUEST)

        return response

    @detail_route()
    def enable(self, request, pk=None):
        """启用用户"""
        try:
            User.objects.get(pk=pk).enable()
            response = Response({}, status=status.HTTP_200_OK)
        except Exception as e:
            response = Response(str(e), status=status.HTTP_400_BAD_REQUEST)

        return response

    @detail_route()
    def disable(self, request, pk=None):
        """禁用用户"""
        try:
            User.objects.get(pk=pk).disable()
            response = Response({}, status=status.HTTP_200_OK)
        except Exception as e:
            response = Response(str(e), status=status.HTTP_400_BAD_REQUEST)

        return response

    @detail_route()
    def menus(self, request, pk=None):
        """用户菜单"""
        try:
            user_menus = User.objects.get(pk=pk).menus.all()
            response_context = {
                "user": pk,
                "menus": map(lambda m: m.as_dict(), user_menus)
            }

            response = Response(response_context, status=status.HTTP_200_OK)
        except Exception as e:
            response = Response(str(e), status=status.HTTP_400_BAD_REQUEST)

        return response


class GroupViewSet(viewsets.ModelViewSet):
    """用户组接口"""
    serializer_class = GroupSerializer
    queryset = Group.objects.all()
    authentication_classes = (SessionAuthentication, TokenAuthentication, )
    permission_classes = (IsAuthenticated, ApiAccessPermission, )


class PermissionViewSet(viewsets.ReadOnlyModelViewSet):
    """权限接口"""
    serializer_class = PermissionSerializer
    queryset = Permission.objects.all()
    authentication_classes = (SessionAuthentication, TokenAuthentication, )
    permission_classes = (IsAuthenticated, ApiAccessPermission, )

    def get_queryset(self):
        custompermissions = ContentType.objects.get(model="custompermissions")
        return Permission.objects.filter(content_type=custompermissions)
