# -*- coding: UTF-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers
from security.models import AuditLog
from management.apis.serializers import UserSerializer
from django.contrib.contenttypes.models import ContentType

__author__ = "axu"

"""
参考文档：
- [ModelSerializer](http://www.django-rest-framework.org/api-guide/serializers/#modelserializer)
"""


class ContentTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = ContentType
        fields = "__all__"


class AuditLogSerializer(serializers.ModelSerializer):
    """
    Serializer relations 参考文档

    http://www.django-rest-framework.org/api-guide/relations/
    """

    user = UserSerializer()
    content_type = ContentTypeSerializer()

    class Meta:
        model = AuditLog
        fields = "__all__"
