# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from performance.databases.backends.base.sqlparser import SQLParser


class SparkSQLParser(SQLParser):
    """基础SparkSQL情况的sql语句解析器"""

    def __init__(self, arg):
        super(SparkSQLParser, self).__init__()
        self.arg = arg
