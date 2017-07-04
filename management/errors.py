# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from management.settings import settings


class NoneUsernameOrPasswordError(Exception):
    """没有发现用户或者密码错误"""

    def __init__(self, *args, **kwargs):
        super(NoneUsernameOrPasswordError, self).__init__(
            settings.ERROR_MESSAGES["NoneUsernameOrPasswordError"], *args, **kwargs)


class UsernameOrPasswordIncorrectError(Exception):
    """用户名或者密码错误"""

    def __init__(self, *args, **kwargs):
        super(UsernameOrPasswordIncorrectError, self).__init__(
            settings.ERROR_MESSAGES["UsernameOrPasswordIncorrectError"], *args, **kwargs)


class UserIsDisableError(Exception):
    """用户已经被禁用错误"""

    def __init__(self, *args, **kwargs):
        super(UserIsDisableError, self).__init__(
            settings.ERROR_MESSAGES["UserIsDisableError"], *args, **kwargs)
