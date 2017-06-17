# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """
    用户表（扩展基础用户表）

    基础用户表参考：https://docs.djangoproject.com/en/1.11/ref/contrib/auth/#django.contrib.auth.models.User
    """
    created = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)
    modified = models.DateTimeField(verbose_name="修改时间", auto_now=True)

    def __unicode__(self):
        return self.username

    class Meta:
        ordering = ('-modified',)
