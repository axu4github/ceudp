# -*- coding: UTF-8 -*-

__author__ = "axu"

from rest_framework import viewsets
from serializers import MenuSerializer
from management.models import Menu
"""
# 参考文档：
- [Django REST Framswork](http://www.django-rest-framework.org/)
- [ModelViewSet](http://www.django-rest-framework.org/api-guide/viewsets/#modelviewset)
"""


class MenuViewSet(viewsets.ModelViewSet):
    """菜单接口"""

    serializer_class = MenuSerializer
    queryset = Menu.objects.all()

    def get_queryset(self):
        return self.request.user.menus.all()
