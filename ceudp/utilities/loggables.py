# -*- coding: UTF-8 -*-
import logging
from django.conf import settings


class Loggable(object):
    """
    参考：https://docs.djangoproject.com/en/1.11/topics/logging/
    """
    logger = logging.getLogger(settings.LOGGER_NAME)

    def get_message(self, message):
        return "{class_name} {message}".format(class_name=self.__class__.__name__, message=message)

    def log_debug(self, message):
        self.logger.debug(self.get_message(message))

    def log_info(self, message):
        self.logger.info(self.get_message(message))

    def log_warn(self, message):
        self.logger.warning(self.get_message(message))

    def log_error(self, message):
        self.logger.error(self.get_message(message))
