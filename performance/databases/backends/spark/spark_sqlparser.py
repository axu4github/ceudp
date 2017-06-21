# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from performance.databases.backends.base.sqlparser import BaseSQLParser


class SparkSQLParser(BaseSQLParser):
    """基础SparkSQL情况的sql语句解析器"""

    def __init__(self, sql_query):
        super(SparkSQLParser, self).__init__(sql_query)
