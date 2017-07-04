# -*- coding: UTF-8 -*-

__author__ = "axu"

from rest_framework import viewsets, views
from serializers import MenuSerializer, LoginSerializer
from management.models import Menu
"""
# 参考文档：
- [Django REST Framswork](http://www.django-rest-framework.org/)
- [ModelViewSet](http://www.django-rest-framework.org/api-guide/viewsets/#modelviewset)
- [APIView](http://www.django-rest-framework.org/api-guide/views/#class-based-views)
"""


class LoginViewSet(views.APIView):
    """docstring for LoginViewSet"""
    serializers = LoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)  # 校验请求参数
        print serializer.validated_data


class MenuViewSet(viewsets.ModelViewSet):
    """菜单接口"""

    serializer_class = MenuSerializer
    queryset = Menu.objects.all()

    def get_queryset(self):
        return self.request.user.menus.all()
