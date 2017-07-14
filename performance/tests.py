# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import tempfile
from collections import OrderedDict
from django.test import TestCase
from performance.databases.backends.base.sqlparser import BaseSQLParser
from performance.databases.backends.spark.spark_sqlparser import SparkSQLParser
# from performance.hdfs_clients import HDFSClient
from performance.utils import Utils
from performance.settings import settings


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

    def test_generate_execute_sql_upper_or_lower(self):
        """测试生成执行查询大小写"""
        sql = """
            select * from t where name = 'XiaoQiang';
        """

        executed_sql = SparkSQLParser(sql).generate_execute_sql()
        self.assertEqual(
            "SELECT * FROM t WHERE name = 'XiaoQiang' LIMIT 10", executed_sql)


class SparkSQLRunEnvTest(TestCase):
    """Spark SQL 运行环境测试"""
    pass


class SparkSQLClassTest(TestCase):

    def test_sql_func(self):
        # print SparkSQL().sql("select * from people  ;")
        pass


# class UnstructuredDataTest(TestCase):
#     """非结构化数据测试"""

#     def setUp(self):
#         self.hdfs_client = HDFSClient(settings.HDFS_WEB_URL)
#         self.uploaded_file = "{0}/{1}".format(
#             settings.BASE_DIR, "/ceudp/fixtures/unstructured_data.docx")

#     def test_upload_file_to_dir(self):
#         dest = "/test_upload/"
#         self.hdfs_client.upload(dest, self.uploaded_file, overwrite=True)

#         dest_full_path = "{0}{1}".format(
#             dest, os.path.basename(self.uploaded_file))
#         # 判断文件存在
#         self.assertTrue(
#             self.hdfs_client.status(dest_full_path, strict=False) is not None)

#         # 删除已上传文件
#         self.hdfs_client.delete(dest_full_path)

#         # 验证
#         self.assertTrue(
#             self.hdfs_client.status(dest_full_path, strict=False) is None)

#     def test_upload_file(self):
#         dest_full_path = "/test_upload/renamed_unstructured_data.docx"
#         self.hdfs_client.upload(
#             dest_full_path, self.uploaded_file, overwrite=True)
#         # 判断文件存在
#         self.assertTrue(
#             self.hdfs_client.status(dest_full_path, strict=False) is not None)

#         # 删除已上传文件
#         self.hdfs_client.delete(dest_full_path)

#         # 验证
#         self.assertTrue(
#             self.hdfs_client.status(dest_full_path, strict=False) is None)

#     def test_list(self):
#         dest_full_path = "/test_upload/test_list.docx"

#         # 上传文件并判断文件是否上传成功
#         self.hdfs_client.upload(
#             dest_full_path, self.uploaded_file, overwrite=True)
#         self.assertTrue(
#             self.hdfs_client.status(dest_full_path, strict=False) is not None)

#         # 查看该文件并对比文件大小是否相同
#         file_info = self.hdfs_client.list(dest_full_path)
#         self.assertEqual(
#             os.path.getsize(self.uploaded_file),
#             file_info['docs'][0]['length'])

#         # 删除文件并判断文件是否删除成功
#         self.hdfs_client.delete(dest_full_path)
#         self.assertTrue(self.hdfs_client.status(
#             dest_full_path, strict=False) is None)

#     def test_download(self):
#         import tempfile
#         (_, local_path) = tempfile.mkstemp()
#         dest_full_path = "/test_download/test_download.docx"
#         # 上传文件并判断文件是否上传成功
#         self.hdfs_client.upload(
#             dest_full_path, self.uploaded_file, overwrite=True)
#         self.assertTrue(self.hdfs_client.status(
#             dest_full_path, strict=False) is not None)

#         self.hdfs_client.download(dest_full_path, local_path)
#         # 确定文件存在
#         self.assertTrue(os.path.exists(local_path))
#         # 确定文件一致
#         self.assertEqual(os.path.getsize(local_path),
#                          os.path.getsize(self.uploaded_file))

#         # 删除临时文件
#         os.remove(local_path)

#         # 删除文件并判断文件是否删除成功
#         self.hdfs_client.delete(dest_full_path)
#         self.assertTrue(self.hdfs_client.status(
#             dest_full_path, strict=False) is None)

#     def test_write(self):
#         # 读取文件全部内容
#         filedata = open(self.uploaded_file, 'rb').read()
#         filename = os.path.basename(self.uploaded_file)
#         dest_full_path = "/test_write/test_write.docx"

#         # 写内容到hdfs
#         self.hdfs_client.write(
#             dest_full_path, data=filedata, filename=filename)
#         # 查看该文件并对比文件大小是否相同
#         #!# 注意：现在hdfs中文件名应为 test_write.docx，本地文件名为 unstructured_data.docx
#         file_info = self.hdfs_client.list(dest_full_path)
#         self.assertEqual(os.path.getsize(
#             self.uploaded_file), file_info['docs'][0]['length'])

#         # 删除文件并判断文件是否删除成功
#         self.hdfs_client.delete(dest_full_path)
#         self.assertTrue(self.hdfs_client.status(
#             dest_full_path, strict=False) is None)

#     def test_search(self):
#         local_path = "{0}/{1}".format(
#             settings.BASE_DIR, "/ceudp/fixtures/people.txt")
#         hdfs_path = "/test_search/"
#         self.hdfs_client.upload(hdfs_path, local_path, overwrite=True)
#         self.assertTrue(
#             self.hdfs_client.status(hdfs_path + "people.txt", strict=False) is not None)

#         result = self.hdfs_client.search("Michael", limit=1)
#         file_name = os.path.basename(local_path)
#         file_extension = Utils.file_extension(file_name)
#         file_size = os.path.getsize(local_path)

#         self.assertEqual(result['docs'][0]['filename'], file_name)
#         self.assertEqual(result['docs'][0]['fileExtension'], file_extension)
#         self.assertEqual(result['docs'][0]['length'], file_size)

#         self.hdfs_client.delete(hdfs_path + "people.txt")
#         self.assertTrue(
#             self.hdfs_client.status(hdfs_path + "people.txt", strict=False) is None)

#         result = self.hdfs_client.search("Michael", limit=1)
#         self.assertEqual(result['numFound'], 0, result)


class UtilsTest(TestCase):
    '''工具类测试'''

    def test_excel_get_contents(self):
        excelfile = "{0}/{1}".format(
            settings.BASE_DIR, "/ceudp/fixtures/callinfo.xlsx")
        self.assertTrue("dy-gz" in Utils.excel_get_contents(excelfile))

    def test_pdf_get_contents(self):
        pdffile = "{0}/{1}".format(
            settings.BASE_DIR, "/ceudp/fixtures/ant_install_doc.pdf")
        self.assertTrue("ant" in Utils.pdf_get_contents(pdffile))

    def test_docx_get_contents(self):
        docxfile = "{0}/{1}".format(
            settings.BASE_DIR, "/ceudp/fixtures/unstructured_data.docx")
        self.assertTrue("非结构化" in Utils.docx_get_contents(docxfile))

    def test_file_get_contents(self):
        file = "{0}/{1}".format(
            settings.BASE_DIR, "/ceudp/fixtures/people.json")
        self.assertTrue("Michael" in Utils.file_get_contents(file))

    # 自动识别文件类型
    def test_get_contents(self):
        file = "{0}/{1}".format(
            settings.BASE_DIR, "/ceudp/fixtures/ant_install_doc.pdf")
        self.assertTrue("ant" in Utils.get_contents(file))

    def test_file_put_contexts(self):
        file = "{0}/{1}".format(tempfile.mkdtemp(), "123.txt")
        Utils.file_put_contents(file, "123")
        self.assertTrue(os.path.exists(file))
        self.assertEqual("123", Utils.get_contents(file))
