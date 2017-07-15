# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from django.forms.models import model_to_dict
from django.contrib.auth.models import AbstractUser
from management.settings import settings
from rest_framework.authtoken.models import Token

__author__ = "axu"

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
    menus = models.ManyToManyField("Menu", verbose_name="用户菜单", blank=True)
    verbose_name = models.CharField(
        verbose_name="显示名称", max_length=50, blank=False, default="")

    def get_or_create_token(self):
        """获取或者创建用户Token"""
        try:
            token = Token.objects.get(user=self)
        except ObjectDoesNotExist:
            token = Token.objects.create(user=self)

        return token

    def post_created(self):
        """创建实例后调用方法，详见 management.signals.py 文件"""
        if not self.is_active:
            self.is_active = True

        if 0 == len(self.password):
            self.set_password(settings.USER_DEFAULT_PASSWORD)

        self.save()

    def enable(self):
        """启用用户"""
        if not self.is_active:
            self.is_active = True

        self.save()

        return self

    def disable(self):
        """禁用用户"""
        if self.is_active:
            self.is_active = False

        self.save()

        return self

    def __unicode__(self):
        return self.username

    class Meta:
        ordering = ('-modified', )


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

    def as_dict(self):
        """模型转换成为Dict"""
        # model_to_dict 方法无法转换 Editable=False 的字段
        # 例如含有 auto_now_add=True 的字段
        instance_dict = model_to_dict(self)
        instance_dict["created"] = self.created
        instance_dict["modified"] = self.modified
        return instance_dict

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


class CustomPermissions(models.Model):
    """自定义权限表"""

    class Meta:
        default_permissions = ()  # 禁用默认权限
        permissions = (
            ("post:management_api:user-list", "用户创建"),
            ("get:management_api:user-list", "用户列表查看"),
            ("get:management_api:user-detail", "用户详情查看"),
            ("get:management_api:user-menus", "用户菜单查看"),
            ("get:management_api:user-enable", "用户启用"),
            ("get:management_api:user-disable", "用户禁用"),
            ("put:management_api:user-detail", "用户信息修改"),
            ("patch:management_api:user-detail", "用户信息部分修改"),
            ("post:management_api:user-change-password", "用户密码修改"),
            ("post:performance_api:query-list", "查询"),
            ("get:performance_api:query-list", "查询历史记录查看"),
            ("get:performance_api:query-detail", "查询历史记录详情查看"),
            ("get:management_api:group-list", "用户组列表查看"),
            ("get:management_api:group-detail", "用户组详情查看"),
            ("get:management_api:permission-list", "权限列表查看"),
            ("get:security_api:auditlog-list", "审计日志列表查看")
        )
