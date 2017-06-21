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
        self.sql_query = sql_query

    def flat_tokens(self, parsed):
        """将所有的token扁平化放在一个生成器中"""
        for item in parsed.tokens:
            if item.is_group:
                for x in self.flat_tokens(item):
                    yield x
            else:
                yield item

    def format(self, **kwargs):
        """格式化SQL"""
        sql = ""
        parsed = sqlparse.parse(self.sql_query)[0]
        for item in self.flat_tokens(parsed):
            item_type = item.ttype
            if item_type is Newline:
                pass
            elif item_type is Whitespace:
                sql += " "
            else:
                sql += item.value

        return sqlparse.format(sql.strip(), **kwargs)
