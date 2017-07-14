# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import sys
from django.conf import settings
from appconf import AppConf


class PerformanceConfigurtion(AppConf):
    """
    Performance应用配置文件

    注意：
    - 不要设置和项目配置（django.conf）同样名称的配置项。
    - 如果设置和项目配置（django.conf）同样名称的配置项，调用时会使用项目配置文件中指定的配置项，而不会使用当前类中的配置项。
    """

    # 成功和失败标志
    FAILED = "-1"
    SUCCESS = "0"

    # Query状态字典
    QUERY_STASTUS = {
        FAILED: "failed",
        SUCCESS: "success",
    }

    # Query表状态信息
    QUERY_STATUS_CHOICES = ((k, v) for k, v in QUERY_STASTUS.items())

    # SPARK_ENVS
    SPARK_MASTER = "spark://axumatoMacBook-Pro.local:7077"

    SPARK_HOME = "/Users/axu/opt/spark-2.0.2-bin-hadoop2.6"
    PYSPARK_DIR = os.path.normpath(SPARK_HOME + "/python")
    PY4J_DIR = os.path.normpath(SPARK_HOME + "/python/lib/py4j-0.10.3-src.zip")
    CONF_SPARK_EXECUTOR_MEMORY = 6
    CONF_SPARK_EXECUTOR_CORES = 2

    SPARK_CONFS = {
        "spark.executor.memory": "{sem}g".format(sem=CONF_SPARK_EXECUTOR_MEMORY),
        "spark.executor.cores": CONF_SPARK_EXECUTOR_CORES,
    }

    sys.path.insert(0, PYSPARK_DIR)
    sys.path.insert(0, PY4J_DIR)

    if "SPARK_HOME" not in os.environ:
        os.environ["SPARK_HOME"] = SPARK_HOME

    # Spark执行程序日志级别
    SPARK_LOG_LEVEL = "ERROR"

    # SPARK_ENVS -EOF-

    # SQLParser 配置
    PER_PAGE_ROWS = 10  # 单页显示记录数
    # SQLParser -EOF-

    # HDFS settings
    HDFS_WEB_URL = "http://10.0.3.49:50070"  # HDFS WEB 访问地址
    HDFS_ROOT_DIR = "/queryengine"  # 应用HDFS根目录
    HDFS_UNSTRUCTURED_DATA_DIR = "{0}/{1}".format(
        HDFS_ROOT_DIR, "unstructured_datas")

    from hdfs.client import Client
    HDFS_CLIENT = Client(HDFS_WEB_URL)

    # Solr settings
    SOLR_URL = "localhost:8983"
    SOLR_COLLECTIONS = "collection1"
    from solrcloudpy.connection import SolrConnection
    SOLR_CONNECTION = SolrConnection(SOLR_URL)[SOLR_COLLECTIONS]

    # 文件类型后缀
    EXCEL_EXTENSIONS = ['.xlsx']
    DOCX_EXTENSIONS = ['.docx']
    PDF_EXTENSIONS = ['.pdf']

    class Meta:
        """如果设置了前缀那么，调用配置的时候也要加上前缀调用。"""
        prefix = ""
