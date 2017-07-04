# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from management.settings import settings


class NoneUsernameOrPasswordError(Exception):
    """没有发现用户或者密码错误"""

    def __init__(self, *args, **kwargs):
        super(NoneUsernameOrPasswordError, self).__init__(
            settings.ERROR_MESSAGES["NoneUsernameOrPasswordError"], *args, **kwargs)
