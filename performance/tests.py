# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.test import TestCase
from performance.databases.backends.base.sqlparser import BaseSQLParser
import sqlparse


class BaseSQLParserTest(TestCase):

    def test_format_func(self):
        sql = """
            select username, 


                passwd, * from table_a as       ta, A,            B, (select      * from  
                table_b as tb);
        """
        formated = BaseSQLParser(sql).formated
        self.assertEqual(
            formated, "SELECT username, passwd, * FROM table_a AS ta, A, B, (SELECT * FROM table_b AS tb);", formated)

    def test_formart_main_construction_func(self):
        sql = """
            select username, 


                passwd, * from table_a as       ta, A,            B, (select      * from  
                table_b as tb) 
            group by A.a, B.a    order by tb.a 
            limit 1
            offset 2
                ;
        """
        main_construction = BaseSQLParser(sql).main_construction
        self.assertTrue("ORDER BY" in main_construction, main_construction)
        self.assertTrue("OFFSET" in main_construction, main_construction)
        self.assertEqual(
            2, int("".join(main_construction.get("OFFSET")).strip()), int("".join(main_construction.get("OFFSET")).strip()))


class SparkSQLRunEnvTests(TestCase):
    """Spark SQL 运行环境测试"""
    pass
