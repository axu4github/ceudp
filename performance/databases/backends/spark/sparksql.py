# -*- coding: utf-8 -*-
from performance.settings import settings
from performance.databases.backends.spark.spark_sqlparser import SparkSQLParser
from ceudp.utilities.loggables import Loggable
from pyspark.sql import SparkSession
from pyspark import SparkConf
from time import time


class SparkSQLBackend(Loggable):
    """
    SparkSQL 执行引擎

    参考文档：http://spark.apache.org/docs/latest/api/python/pyspark.sql.html
    """

    def __init__(self, *arg, **kwargs):
        super(SparkSQLBackend, self).__init__(*arg, **kwargs)
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

    def perform_sql(self, sql_query):
        """执行SQL查询，返回执行时间和结果"""
        start_microsecond = time()  # 毫秒
        query_set = self.spark.sql(sql_query).collect()
        duration = time() - start_microsecond
        return (duration, query_set)

    def count(self, sql_query):
        """获取查询总数"""
        pass

    def pagination(self, start=0):
        """分页"""
        pass

    def sql(self, sql_query):
        """SQL查询"""
        sqlparser = SparkSQLParser(sql_query)
        start = sqlparser.start()
        (count_duration, rows) = self.count(sqlparser.count())
        (perform_duration, query_set) = self.perform_sql(sqlparser.executed())
        (page_duration, paged_query_set) = self.pagination(query_set, start)
        duration = count_duration + perform_duration + page_duration
        return {
            "rows": rows,  # 查询总数量
            "duration": duration,  # 查询时间
            "start": start,  # 分页起始数量
            "executed_query": sqlparser.format(),  # 执行查询语句
            "data": paged_query_set,  # 查询结果集
        }
