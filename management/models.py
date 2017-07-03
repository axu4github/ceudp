# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import AbstractUser

"""
字段类型参考：
https://docs.djangoproject.com/en/1.11/ref/models/fields/
"""


class User(AbstractUser):
    """
    用户表（扩展基础用户表）

    基础用户表参考：https://docs.djangoproject.com/en/1.11/ref/contrib/auth/#django.contrib.auth.models.User
    """
    created = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)
    modified = models.DateTimeField(verbose_name="修改时间", auto_now=True)
    menus = models.ManyToManyField("Menu", verbose_name="用户菜单")

    def __unicode__(self):
        return self.username

    class Meta:
        ordering = ('-modified',)


class Menu(models.Model):
    """菜单表"""

    name = models.CharField(verbose_name="菜单名称", max_length=20, blank=False)
    code = models.CharField(verbose_name="菜单代码", max_length=20, blank=False)
    parent = models.ForeignKey(
        "self", default=0, blank=False, related_name="child")
    is_leaf = models.BooleanField(
        verbose_name="是否为子节点", default=False, blank=False)
    linkto = models.CharField(verbose_name="链接地址", max_length=50, default="#")
    created = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)
    modified = models.DateTimeField(verbose_name="修改时间", auto_now=True)

    def __unicode__(self):
        return self.name
