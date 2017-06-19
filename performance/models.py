# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from management.models import User
from performance.settings import settings

"""
字段类型参考：
https://docs.djangoproject.com/en/1.11/ref/models/fields/
"""


class Query(models.Model):
    """查询表"""
    query = models.TextField(verbose_name="查询内容", blank=False, default="")
    excuted_query = models.TextField(verbose_name="执行的查询", default="")
    created = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)
    duration = models.FloatField(verbose_name="执行时长", default=0.0)
    total = models.IntegerField(verbose_name="查询结果数量", default=0)
    status = models.CharField(verbose_name="查询状态", max_length=2, choices=settings.QUERY_STATUS_CHOICES, default=settings.FAILED)
    error_messages = models.TextField(verbose_name="查询错误", blank=True, default="")
    user = models.ForeignKey(User, verbose_name="执行人")

    def __unicode__(self):
        return self.query

    class Meta:
        ordering = ('-created',)
