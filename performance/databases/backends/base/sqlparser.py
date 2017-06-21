# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import sqlparse
from ceudp.utilities.loggables import Loggable
from sqlparse.tokens import Whitespace, Newline

"""
# 参考文档
- https://sqlparse.readthedocs.io/en/latest/
"""


class BaseSQLParser(Loggable):
    """基础SQL解析器"""

    def __init__(self, sql_query):
        super(BaseSQLParser, self).__init__()
        self.sql_query = sql_query  # 原始SQL
        self.formated = self.format(keyword_case="upper")  # 格式化后的SQL

    def format(self, **kwargs):
        """
        格式化SQL
        **kwargs 参数参考文档：https://sqlparse.readthedocs.io/en/latest/api/#formatting
        """
        sql = ""
        for item in sqlparse.parse(self.sql_query)[0].flatten():
            item_type = item.ttype
            if item_type is Newline:
                pass
            elif item_type is Whitespace:
                sql += " "
            else:
                sql += item.value

        return sqlparse.format(sql.strip(), **kwargs)
