# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import sqlparse
from sqlparse.tokens import Whitespace, Newline, Keyword, DML, Punctuation
from ceudp.utilities.loggables import Loggable
from collections import OrderedDict

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
        self.main_construction = self.formart_main_construction()

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

        sql = sqlparse.format(sql.strip(), **kwargs)
        # 如果不存在分号（`;`），则在最后添加分号（`;`）。
        if ";" not in sql and ";" != sql.endswith():
            sql += ";"

        return sql

    def formart_main_construction(self):
        """
        # 获取SQL的主结构（一级）

        # 限制：
        - 1. 只格式化了一级，没有嵌套格式化
        - 2. SQL最后必须有分号（`;`）, 因为判断是按照分号（`;`）结算，若没有分号则最后一部分是无法被添加到`DICT`中。
        - 3. 没有识别`Where`条件

        ```
        # 举例：
        原始SQL => "SELECT * FROM table as t WHERE t.a='1' AND t.b='2' GROUP BY t.c ORDER BY t.d DESC LIMIT 1 OFFSET 2;";
        格式化后为 => 
        OrderedDict([
            (u'SELECT', [u' ', u'*', u' ']), 
            (u'FROM', [u' ', u'TABLE', u' ', u'AS', u' ', u't', u' ', u"WHERE t.a='1' AND t.b='2' "]), 
            (u'GROUP BY', [u' ', u't.c', u' ']), 
            (u'ORDER BY', [u' ', u't.d DESC', u' ']), 
            (u'LIMIT', [u' ', u'1', u' ']), 
            (u'OFFSET', [u' ', u'2']), 
            (u';', [u';'])
        ])
        ```
        """
        main_construction = OrderedDict()
        is_append = True  # 为了处理`GROUP BY` 和 `ORDER BY` 中间的空格
        for item in sqlparse.parse(self.formated)[0].tokens:
            # 处理 `SELECT`
            if item.ttype is DML and "SELECT" == item.value.upper():
                tmp_values = []
                current_keyword = item.value
            # 处理 `Keyword` (`FORM`, `LIMIT`, `OFFSET`)
            elif item.ttype is Keyword and item.value.upper() in ["FROM", "LIMIT", "OFFSET"]:
                main_construction[current_keyword] = tmp_values
                tmp_values = []
                current_keyword = item.value
            # 处理 `Keyword` (`GROUP`, `ORDER`)
            elif item.ttype is Keyword and item.value.upper() in ["GROUP", "ORDER"]:
                main_construction[current_keyword] = tmp_values
                tmp_values = []
                current_keyword = item.value
                is_append = False
            # 处理 `Keyword` (`GROUP BY`, `ORDER BY`)
            elif item.ttype is Keyword and "BY" == item.value.upper():
                current_keyword = current_keyword + " " + item.value
                is_append = True
            # 处理分号 `;`
            elif item.ttype is Punctuation and ";" == item.value:
                main_construction[current_keyword] = tmp_values
                main_construction[item.value] = []
            # 处理值和空格（`Whitespace`）
            else:
                if is_append:
                    tmp_values.append(item.value)

        return main_construction

    def print_main_construction(self, main_construction=None):
        """通过主结构对象返回SQL"""
        sql = ""

        if main_construction is None:
            main_construction = self.main_construction

        for keyword, values in main_construction.items():
            sql += keyword + "".join(values)

        return sql
