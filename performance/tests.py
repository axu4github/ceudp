# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.test import TestCase
from performance.databases.backends.base.sqlparser import BaseSQLParser
import sqlparse


class BaseSQLParserTest(TestCase):

    def test_format(self):
        sql = """
            select username, 


                passwd, * from table_a as       ta, A,            B, (select      * from  
                table_b as tb);
        """
        formated = BaseSQLParser(sql).formated
        self.assertEqual(
            formated, "SELECT username, passwd, * FROM table_a AS ta, A, B, (SELECT * FROM table_b AS tb);", formated)


class SparkSQLRunEnvTests(TestCase):
    """Spark SQL 运行环境测试"""
    pass
