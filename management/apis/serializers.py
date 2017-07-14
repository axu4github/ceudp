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


class PermissionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Permission
        fields = ["id", "codename", "name"]


class GroupSerializer(serializers.ModelSerializer):
    permissions = PermissionSerializer(many=True, read_only=True)

    class Meta:
        model = Group
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    # groups = GroupSerializer(many=True, read_only=True)
    # user_permissions = PermissionSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ("id", "email", "username", "verbose_name", "is_active",
                  "last_login", "created", "modified", "groups", "user_permissions")


class PasswordSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["password", ]
