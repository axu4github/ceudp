# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth import authenticate as django_authenticate
from management.errors import NoneUsernameOrPasswordError, UsernameOrPasswordIncorrectError, UserIsDisableError

__author__ = "axu"


class Authentication(object):
    """用户认证"""

    @staticmethod
    def authenticate(username=None, password=None):
        if username is None or password is None:
            raise NoneUsernameOrPasswordError()

        user = django_authenticate(username=username, password=password)

        if user is None:
            raise UsernameOrPasswordIncorrectError()

        if not user.is_active:
            raise UserIsDisableError()

        return True
