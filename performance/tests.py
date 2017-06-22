# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import sqlparse
from collections import OrderedDict
from django.test import TestCase
from performance.databases.backends.base.sqlparser import BaseSQLParser
from performance.databases.backends.spark.spark_sqlparser import SparkSQLParser


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
            2, int("".join(main_construction.get("OFFSET")).strip()), main_construction)
        self.assertTrue(";" in main_construction, main_construction)

    def test_print_main_construction_func(self):
        sql = """
            select username, 


                passwd, * from table_a as       ta, A,            B, (select      * from  
                table_b as tb) 
            group by A.a, B.a    order by tb.a 
            limit 1
            offset 2
                ;
        """
        sqlparser = BaseSQLParser(sql)
        mc = sqlparser.main_construction
        self.assertTrue(isinstance(mc, OrderedDict), mc)

        mc_sql = sqlparser.print_main_construction(mc)
        self.assertEqual(sqlparser.formated, mc_sql, mc_sql)


class SparkSQLParserTest(TestCase):

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
        main_construction = SparkSQLParser(sql).main_construction
        self.assertTrue(";" not in main_construction, main_construction)
        self.assertTrue("LIMIT" not in main_construction, main_construction)

    def test_generate_execute_sql_func(self):
        sql = "select * from t limit 10"
        executed_sql = SparkSQLParser(sql).generate_execute_sql()
        self.assertEqual("SELECT * FROM t LIMIT 10", executed_sql)

        sql = "select * from t limit 30"
        executed_sql = SparkSQLParser(sql).generate_execute_sql()
        self.assertEqual("SELECT * FROM t LIMIT 20", executed_sql)

        sql = "select * from t limit 30"
        executed_sql = SparkSQLParser(sql, 2).generate_execute_sql()
        self.assertEqual("SELECT * FROM t LIMIT 30", executed_sql)

        sql = "select t.a as a from t"
        executed_sql = SparkSQLParser(sql, 2).generate_execute_sql()
        self.assertEqual("SELECT t.a AS a FROM t LIMIT 40", executed_sql)

    def test_generate_count_sql_func(self):
        sql = "select sum(t.a) as sum_a from t group by t.a"
        count_sql = SparkSQLParser(sql).generate_count_sql()
        self.assertEqual(
            "SELECT sum(t.a) AS sum_a FROM t GROUP BY t.a", count_sql[0])
        self.assertTrue(count_sql[1])

        sql = "select count(t.a) from t group by t.a order by t.b limit 10"
        count_sql = SparkSQLParser(sql).generate_count_sql()
        self.assertEqual(
            "SELECT count(t.a) FROM t GROUP BY t.a LIMIT 10", count_sql[0])
        self.assertTrue(count_sql[1])

        sql = "select * from t limit 10"
        count_sql = SparkSQLParser(sql).generate_count_sql()
        self.assertEqual("SELECT * FROM t LIMIT 10", count_sql[0])
        self.assertTrue(count_sql[1])

        sql = "select * from t order by t.a  "
        count_sql = SparkSQLParser(sql).generate_count_sql()
        self.assertEqual("SELECT COUNT(*) AS cnt FROM t", count_sql[0])
        self.assertTrue(not count_sql[1])


class SparkSQLRunEnvTests(TestCase):
    """Spark SQL 运行环境测试"""
    pass
