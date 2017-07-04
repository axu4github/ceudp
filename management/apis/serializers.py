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
        fields = ["name", "code", "parent", "linkto", ]


class LoginSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["username", "password", ]
