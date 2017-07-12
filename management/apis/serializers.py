# -*- coding: UTF-8 -*-
from rest_framework import serializers
from management.models import Menu, User
from django.contrib.auth.models import Permission, Group

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


class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = "__all__"


class PermissionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Permission
        fields = ["id", "codename", "name"]
