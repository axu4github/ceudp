# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from management.models import User
from performance.settings import settings
from performance.databases.backends.spark.sparksql import SparkSQL
from django.forms.models import model_to_dict

"""
# 参考文档
- [字段类型](https://docs.djangoproject.com/en/1.11/ref/models/fields/)
"""


class Query(models.Model):
    """查询表"""
    query = models.TextField(verbose_name="查询内容", blank=False)
    executed_query = models.TextField(verbose_name="执行的查询", default="")
    page_number = models.IntegerField(verbose_name="页数", default=1)
    created = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)
    duration = models.FloatField(verbose_name="执行时长", default=0.0)
    rows = models.IntegerField(verbose_name="查询结果数量", default=0)
    status = models.CharField(verbose_name="查询状态", max_length=2, choices=settings.QUERY_STATUS_CHOICES, default=settings.FAILED)
    error_messages = models.TextField(verbose_name="查询错误", blank=True, default="")
    user = models.ForeignKey(User, verbose_name="执行人")

    def execute(self, page_number=1):
        if self.query is None:
            raise Exception("param query is None.")

        return SparkSQL().sql(self.query, page_number)

    def as_dict(self):
        """模型转换成为Dict"""
        # model_to_dict 方法无法转换 Editable=False 的字段
        # 例如含有 auto_now_add=True 的字段
        instance_dict = model_to_dict(self)
        instance_dict["created"] = self.created
        return instance_dict

    def __unicode__(self):
        return self.query

    class Meta:
        ordering = ('-created',)
