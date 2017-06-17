# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
import sys
from django.conf import settings
from appconf import AppConf
from hdfs.client import Client


class Settings(AppConf):
    """
    Performance应用配置文件

    注意：
    - 不要设置和项目配置（django.conf）同样名称的配置项。
    - 如果设置和项目配置（django.conf）同样名称的配置项，调用时会使用项目配置文件中指定的配置项，而不会使用当前类中的配置项。
    """
    class Meta:
        """如果设置了前缀那么，调用配置的时候也要加上前缀调用。"""
        prefix = ""
