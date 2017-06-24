# -*- coding: utf-8 -*-
from performance.settings import settings
from performance.databases.backends.spark.spark_sqlparser import SparkSQLParser
from ceudp.utilities.loggables import Loggable
from pyspark.sql import SparkSession
from pyspark import SparkConf
from time import time


class SparkSQL(Loggable):
    """
    SparkSQL 执行引擎

    参考文档：http://spark.apache.org/docs/latest/api/python/pyspark.sql.html
    """

    def __init__(self, *arg, **kwargs):
        super(SparkSQL, self).__init__(*arg, **kwargs)
        self._init_spark_conf(*arg, **kwargs)
        self._init_spark_session(*arg, **kwargs)

    def _init_spark_conf(self, *arg, **kwargs):
        """初始化SparkConf"""
        self.spark_conf = SparkConf() \
            .setAppName(settings.DEFAULT_APPLICATION_NAME) \
            .setMaster(settings.SPARK_MASTER)

        if settings.SPARK_CONFS is not None:
            for k, v in settings.SPARK_CONFS.items():
                self.spark_conf.set(k, v)

    def _init_spark_session(self, *arg, **kwargs):
        """获取或者申请SparkSession"""
        self.spark = SparkSession.builder \
            .config(conf=self.spark_conf) \
            .enableHiveSupport() \
            .getOrCreate()

        self.spark.sparkContext.setLogLevel('ERROR')

    def get_spark_session(self):
        return self.spark

    def perform_sql(self, sql_query):
        """执行SQL查询，返回执行时间和结果"""
        start_microsecond = time()  # 毫秒
        df = self.spark.sql(sql_query)  # data frame
        columns = df.columns
        query_set = df.collect()
        duration = time() - start_microsecond
        return (duration, query_set, columns)

    def count(self, count_sql, need_count=True):
        """获取查询总数"""
        start_microsecond = time()  # 毫秒
        if need_count:
            total = int(self.spark.sql(count_sql).count())
        else:
            total = int(self.spark.sql(count_sql).collect()[0].asDict()['cnt'])

        duration = time() - start_microsecond
        return (duration, total)

    def pagination(self, query_set, start, end):
        """
        分页

        `pagination` 单词出处（http://www.django-rest-framework.org/api-guide/pagination/）
        """
        start_microsecond = time()  # 毫秒
        paged = query_set[start:end]
        duration = time() - start_microsecond
        return (duration, paged)

    def sql(self, sql_query, page_number=1):
        """SQL查询"""

        # 解析SQL
        sqlparser = SparkSQLParser(sql_query, page_number)

        # 执行查询总数
        (count_sql, need_count) = sqlparser.generate_count_sql()
        (count_duration, total) = self.count(count_sql, need_count)
        self.log_info(
            "- COUNT SQL: {s}, DURATION: {d}".format(s=count_sql, d=count_duration))

        # 执行查询条件
        sql_query = sqlparser.generate_execute_sql()
        (perform_duration, query_set, columns) = self.perform_sql(sql_query)
        self.log_info(
            "- EXECUTE SQL: {s}, DURATION: {d}".format(s=sql_query, d=perform_duration))

        # 进行分页
        (start, end) = sqlparser.get_pagination()
        (page_duration, paged_query_set) = self.pagination(query_set, start, end)
        self.log_info(
            "- PAGINATION DURATION: {d}".format(d=page_duration))

        # 计算查询时长
        duration = count_duration + perform_duration + page_duration

        return {
            "total": total,  # 查询总数量
            "duration": duration,  # 查询时间
            "page_number": page_number,  # 分页起始数量
            "executed_query": sqlparser.format(),  # 执行查询语句
            "columns": columns,
            "data": paged_query_set,  # 查询结果集
        }
