# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.authtoken.models import Token

"""
字段类型参考：
https://docs.djangoproject.com/en/1.11/ref/models/fields/

多对多模型参考:
https://docs.djangoproject.com/en/1.11/topics/db/examples/many_to_many/
"""


class User(AbstractUser):
    """
    用户表（扩展基础用户表）

    基础用户表参考：https://docs.djangoproject.com/en/1.11/ref/contrib/auth/#django.contrib.auth.models.User
    """
    created = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)
    modified = models.DateTimeField(verbose_name="修改时间", auto_now=True)
    menus = models.ManyToManyField("Menu", verbose_name="用户菜单")

    def get_or_create_token(self):
        """获取或者创建用户Token"""
        try:
            token = Token.objects.get(user=self)
        except ObjectDoesNotExist:
            token = Token.objects.create(user=self)

        return token

    def __unicode__(self):
        return self.username

    class Meta:
        ordering = ('-modified',)


class Menu(models.Model):
    """菜单表"""

    name = models.CharField(verbose_name="菜单名称", max_length=20, blank=False)
    code = models.CharField(verbose_name="菜单代码", max_length=20, blank=False)
    parent = models.ForeignKey("self", verbose_name="父菜单",
                               default=0, blank=False, related_name="child")
    is_leaf = models.BooleanField(
        verbose_name="是否为子节点", default=False, blank=False)
    linkto = models.CharField(verbose_name="链接地址", max_length=50, default="#")
    created = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)
    modified = models.DateTimeField(verbose_name="修改时间", auto_now=True)

    def save(self, *args, **kwargs):
        try:
            self.parent
        except ObjectDoesNotExist:
            self.is_leaf = False
        else:
            self.is_leaf = True

        super(Menu, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name
