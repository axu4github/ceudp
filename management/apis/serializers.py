# -*- coding: UTF-8 -*-
from rest_framework import serializers
from management.models import Menu, User
from django.contrib.auth.models import Permission, Group

__author__ = "axu"

"""
参考文档：
- [ModelSerializer](http://www.django-rest-framework.org/api-guide/serializers/#modelserializer)
"""


class MenuSerializer(serializers.ModelSerializer):

    class Meta:
        model = Menu
        fields = "__all__"


class PermissionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Permission
        fields = ["id", "codename", "name"]


class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = ("id", "name", "permissions")


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ("id", "email", "username", "verbose_name", "is_active",
                  "last_login", "created", "modified", "groups", "user_permissions")


class PasswordSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["password", ]
