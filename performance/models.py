# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from management.models import User


class Query(models.Model):
    """查询表"""
    query = models.TextField(verbose_name="查询内容", blank=False, default="")
    excuted_query = models.TextField(verbose_name="执行的查询", default="")
    created = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)
    duration = models.FloatField(verbose_name="执行时长", default=0.0)
    total = models.IntegerField(verbose_name="查询结果数量", default=0)
    error_messages = models.TextField(verbose_name="查询错误", default="")
    user = models.ForeignKey(User, verbose_name="执行人")

    class Meta:
        ordering = ('-created',)
