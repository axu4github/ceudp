# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from performance.databases.backends.base.sqlparser import BaseSQLParser
import sqlparse


class SparkSQLParser(BaseSQLParser):
    """基础SparkSQL情况的sql语句解析器"""

    def __init__(self, sql_query):
        super(SparkSQLParser, self).__init__(sql_query)
        self._init_sparksql()

    def _init_sparksql(self):
        """
        初始化符合SparkSQL标准的sql语句

        # 规则
        - 1. 若存在`;`号，则删除。
        - 2. 若存在`分页语句`，则获取并删除
        """
        self.format = self.remove_semicolon_if_exists()
        self.format = self.get_pagination()

    def start(self):
        """从SQL获取分页参数OFFSET"""
        return 0

    def count(self):
        """得到查询总数语句"""
        pass

    def executed(self):
        """
        得到执行查询语句

        # 规则:
        - 1. 去掉最后的分号(`;`)
        - 2. 判断是否存在分页参数
            - 若存在，则记录并删除该参数
        - 3. 修改或者添加`LIMIT`参数
        """
        pass

    def get_pagination(self):
        pass

    def remove_semicolon_if_exists(self):
        """删除分号"""
        if ";" in self.format:
            return self.format[0:-1]
        else:
            return self.format
