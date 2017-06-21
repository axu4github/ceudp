# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from ceudp.utilities.loggables import Loggable


class SQLParser(Loggable):
    """基础SQL解析器"""

    def __init__(self, arg):
        super(SQLParser, self).__init__()
        self.arg = arg
