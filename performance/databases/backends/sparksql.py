# -*- coding: utf-8 -*-
from performance.settings import settings
from ceudp.utilities.loggables import Loggable
# from pyspark.sql import SparkSession


class SparkSQL(Loggable):
    """
    SparkSQL 执行引擎

    参考文档：http://spark.apache.org/docs/latest/api/python/pyspark.sql.html
    """

    def __init__(self, *arg, **kwargs):
        super(SparkSQL, self).__init__(*arg, **kwargs)

    def sql(self, sql_query):
        return sql_query
