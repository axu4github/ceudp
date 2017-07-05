# -*- coding: UTF-8 -*-
from __future__ import unicode_literals

from serializers import MenuSerializer, UserSerializer, PasswordSerializer
from rest_framework import viewsets, views, status, mixins
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from management.apis.permissions import CustomerAccessPermission
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
    permission_classes = (IsAuthenticated, CustomerAccessPermission, )


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
    permission_classes = (IsAuthenticated, )

    @detail_route(methods=['post'])
    def change_password(self, request, pk=None):
        serializer = PasswordSerializer(data=request.data)
        if serializer.is_valid():
            self.request.user.set_password(serializer.data["password"])
            self.request.user.save()
            return Response({})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
