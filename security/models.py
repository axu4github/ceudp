# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.contenttypes.models import ContentType
from management.models import User


__author__ = "axu"


class ACTION(object):
    """审计日志操作动作"""

    CREATE = "CREATE"  # 创建
    UPDATE = "UPDATE"  # 修改
    DESTROY = "DESTROY"  # 删除
    API_LOGIN = "API_LOGIN"  # 接口登陆
    LOGIN = "LOGIN"  # 网页登陆
    LOGOUT = "LOGOUT"  # 网页登出


class AuditLog(models.Model):
    """审计日志表"""

    user = models.ForeignKey(User, verbose_name="操作用户", blank=False)
    content_type = models.ForeignKey(
        ContentType, verbose_name="操作对象模型", blank=False)
    action = models.CharField(verbose_name="操作动作", max_length=50, blank=False)
    content = models.TextField(verbose_name="操作内容", default="")
    created = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)

    def __unicode__(self):
        return "{user} | {model} | {action} | {content}".format(
            user=self.user, model=self.content_type.model,
            action=self.action, content=self.content)

    class Meta:
        ordering = ('-created', )
