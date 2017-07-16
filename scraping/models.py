# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

__author__ = "axu"

"""
字段类型参考：
https://docs.djangoproject.com/en/1.11/ref/models/fields/

多对多模型参考:
https://docs.djangoproject.com/en/1.11/topics/db/examples/many_to_many/
"""


class ScrapeJob(models.Model):
    """采集任务表"""
    job_name = models.CharField(
        verbose_name="任务名称", max_length=50, blank=False)
    job_type = models.CharField(
        verbose_name="任务类型", max_length=50, blank=False)
    data_source = models.CharField(
        verbose_name="数据源", max_length=200, blank=False)
    destination = models.CharField(
        verbose_name="目的地", max_length=200, blank=False)
    created = models.DateTimeField(
        verbose_name="创建时间", auto_now_add=True)
    modified = models.DateTimeField(
        verbose_name="修改时间", auto_now=True)
    interval = models.CharField(
        verbose_name="采集间隔", max_length=50, default="")
    next_time = models.DateTimeField(
        verbose_name="下次采集时间")
    pid = models.CharField(
        verbose_name="执行采集任务进程号", max_length=50, default="")
    status = models.CharField(
        verbose_name="状态", max_length=50, blank=False, default="NO_RUN")

    class Meta:
        ordering = ('-modified', )
