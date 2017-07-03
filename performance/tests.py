# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from collections import OrderedDict
from django.test import TestCase
from performance.databases.backends.base.sqlparser import BaseSQLParser
from performance.databases.backends.spark.spark_sqlparser import SparkSQLParser


class BaseSQLParserTest(TestCase):

    def test_format_func(self):
        """测试基础SQL解析器，格式化SQL方法"""
        sql = """
            select username, 


                passwd, * from table_a as       ta, A,            B, (select      * from  
                table_b as tb);
        """
        formated = BaseSQLParser(sql).formated
        self.assertEqual(
            formated, "SELECT username, passwd, * FROM table_a AS ta, A, B, (SELECT * FROM table_b AS tb)", formated)

    def test_formart_main_construction_func(self):
        """测试基础SQL解析器 获取主结构方法"""
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
        self.assertTrue(";" not in main_construction, main_construction)

    def test_print_main_construction_func(self):
        """测试基础SQL解析器，打印SQL方法"""
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
        self.assertEqual(sqlparser.formated[0:-1], mc_sql)


class SparkSQLParserTest(TestCase):

    def test_formart_main_construction_func(self):
        """测试SparkSQL解析器，获取主结构方法"""
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

    def test_generate_common_execute_sql(self):
        """测试生成普通查询SQL"""
        sql = "select * from t limit 10;"
        executed_sql = SparkSQLParser(sql).generate_execute_sql()
        self.assertEqual("SELECT * FROM t LIMIT 10", executed_sql)

    def test_generate_common_execute_sql_page_one(self):
        """测试生成普通查询SQL分页第一页"""
        sql = "select * from t limit 30"
        executed_sql = SparkSQLParser(sql).generate_execute_sql()
        self.assertEqual("SELECT * FROM t LIMIT 10", executed_sql)

    def test_generate_common_execute_sql_page_two(self):
        """测试生成普通查询SQL分页第二页"""
        sql = "select * from t limit 30;"
        executed_sql = SparkSQLParser(sql, 2).generate_execute_sql()
        self.assertEqual("SELECT * FROM t LIMIT 20", executed_sql)

    def test_generate_common_execute_sql_select(self):
        """测试生成普通查询SQL含有SELECT条件"""
        sql = "select t.a as a from t"
        executed_sql = SparkSQLParser(sql, 2).generate_execute_sql()
        self.assertEqual("SELECT t.a AS a FROM t LIMIT 20", executed_sql)

    def test_generate_common_execute_sql_where(self):
        """测试生成普通查询SQL含有WHERE条件"""
        sql = "select * from live_on_hive_csr where csrid = \"asdasdasd\";"
        executed_sql = SparkSQLParser(sql).generate_execute_sql()
        self.assertEqual(
            "SELECT * FROM live_on_hive_csr WHERE csrid = \"asdasdasd\" LIMIT 10", executed_sql)

    def test_generate_execute_sql_special_chars(self):
        """测试生成查询SQL含有特殊字符"""
        sql = """
            select\n\t*\nfrom\n(select\n\tcsragentid, count(csragentid) as group_csragentid\nfrom\n\tlive_on_hive_csr\ngroup by\n\tcsragentid) t\norder by\n\tt.group_csragentid DESC;
        """
        executed_sql = SparkSQLParser(sql).generate_execute_sql()
        self.assertEqual(
            "SELECT * FROM (SELECT csragentid, count(csragentid) AS group_csragentid FROM live_on_hive_csr GROUP BY csragentid) t ORDER BY t.group_csragentid DESC LIMIT 10", executed_sql)

    def test_generate_count_sql_groupby(self):
        """测试生成查询总数SQL含有GROUP BY（执行count方法）"""
        sql = "select sum(t.a) as sum_a from t group by t.a"
        count_sql = SparkSQLParser(sql).generate_count_sql()
        self.assertEqual(
            "SELECT sum(t.a) AS sum_a FROM t GROUP BY t.a", count_sql[0])
        self.assertTrue(count_sql[1])

    def test_generate_count_sql_orderby(self):
        """测试生成查询总数SQL含有ORDER BY，带LIMIT（执行count方法）"""
        sql = "select count(t.a) from t group by t.a order by t.b limit 10"
        count_sql = SparkSQLParser(sql).generate_count_sql()
        self.assertEqual(
            "SELECT count(t.a) FROM t GROUP BY t.a LIMIT 10", count_sql[0])
        self.assertTrue(count_sql[1])

    def test_generate_count_sql_limit(self):
        """测试生成查询总数SQL带LIMIT（执行count方法）"""
        sql = "select * from t limit 10"
        count_sql = SparkSQLParser(sql).generate_count_sql()
        self.assertEqual("SELECT * FROM t LIMIT 10", count_sql[0])
        self.assertTrue(count_sql[1])

    def test_generate_count_sql_orderby_not_count(self):
        """测试生成查询总数SQL带ORDER BY 不带LIMIT（不执行count方法）"""
        sql = "select * from t order by t.a  "
        count_sql = SparkSQLParser(sql).generate_count_sql()
        self.assertEqual("SELECT COUNT(*) AS cnt FROM t", count_sql[0])
        self.assertTrue(not count_sql[1])

    def test_generate_count_sql_where(self):
        """测试生成查询总数SQL带WHERE条件"""
        sql = "select * from live_on_hive_csr where csrid = \"asdasdasd\";"
        count_sql = SparkSQLParser(sql).generate_count_sql()
        self.assertEqual(
            "SELECT COUNT(*) AS cnt FROM live_on_hive_csr WHERE csrid = \"asdasdasd\"", count_sql[0])
        self.assertTrue(not count_sql[1])

    def test_generate_count_sql_special_chars(self):
        """测试生成查询SQL含有特殊字符"""
        sql = """
            select\n\t*\nfrom\n(select\n\tcsragentid, count(csragentid) as group_csragentid\nfrom\n\tlive_on_hive_csr\ngroup by\n\tcsragentid) t\norder by\n\tt.group_csragentid DESC;
        """
        (count_sql, need_count) = SparkSQLParser(sql).generate_count_sql()
        self.assertEqual(
            "SELECT COUNT(*) AS cnt FROM (SELECT csragentid, count(csragentid) AS group_csragentid FROM live_on_hive_csr GROUP BY csragentid) t", count_sql)
        self.assertTrue(not need_count)


class SparkSQLRunEnvTest(TestCase):
    """Spark SQL 运行环境测试"""
    pass


class SparkSQLClassTest(TestCase):

    def test_sql_func(self):
        # print SparkSQL().sql("select * from people  ;")
        pass
