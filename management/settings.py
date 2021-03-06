# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from appconf import AppConf

__author__ = "axu"


class ManagementConfigurtion(AppConf):
    """
    Management应用配置文件

    注意：
    - 不要设置和项目配置（django.conf）同样名称的配置项。
    - 如果设置和项目配置（django.conf）同样名称的配置项，调用时会使用项目配置文件中指定的配置项，而不会使用当前类中的配置项。
    """

    # 错误提示信息
    ERROR_MESSAGES = {
        "NoneUsernameOrPasswordError": "none username or passoword.",
        "UsernameOrPasswordIncorrectError": "username or password were incorrect.",
        "UserIsDisableError": "user has been disabled.",
    }

    # 用户默认密码
    USER_DEFAULT_PASSWORD = "123456"

    class Meta:
        """如果设置了前缀那么，调用配置的时候也要加上前缀调用。"""
        prefix = ""
