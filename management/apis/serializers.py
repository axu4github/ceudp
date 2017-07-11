# -*- coding: UTF-8 -*-
from rest_framework import serializers
from management.models import Menu, User

"""
参考文档：
- [ModelSerializer](http://www.django-rest-framework.org/api-guide/serializers/#modelserializer)
"""


class MenuSerializer(serializers.ModelSerializer):

    class Meta:
        model = Menu
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["id", "email", "username", "verbose_name", "is_active",
                  "last_login", "created", "modified", "menus", ]


class PasswordSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["password", ]
