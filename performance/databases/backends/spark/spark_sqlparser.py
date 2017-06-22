# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from performance.databases.backends.base.sqlparser import BaseSQLParser
from performance.settings import settings


class SparkSQLParser(BaseSQLParser):
    """基础SparkSQL情况的sql语句解析器"""

    def __init__(self, sql_query, page_number=1):
        if int(page_number) < 1 or not isinstance(page_number, int):
            raise Exception("page_number invalid")

        self.page_number = int(page_number)
        self.per_page_rows = settings.PER_PAGE_ROWS
        self.limit = None

        super(SparkSQLParser, self).__init__(sql_query)

    def formart_main_construction(self):
        """
        [override]

        # 重写父类 `formart_main_construction()` 方法
        # 初始化符合SparkSQL标准的main_construction对象

        # 规则
        - 若存在`;`号，则删除
        - 若存在`LIMIT`，则获取值并删除 (self.limit)
        """
        mc = super(SparkSQLParser, self).formart_main_construction()
        mc = self.remove_semicolon_if_exists(mc)
        mc = self.init_and_remove_limit_if_exists(mc)
        return mc

    def generate_count_sql(self):
        """
        # 生成查询总数语句

        # 规则
        - 若存在`ORDER BY`，去除`ORDER BY`
        - 若存在`GROUP BY`，则直接返回，而后进行count()
        - 若不存在`GROUP BY`，且若存在`LIMIT`，则直接返回
        - 若既不存在`GROUP BY`，且不存在`LIMIT`则将`SELECT`和`FROM`中间的内容替换成为`COUNT(*) AS cnt`
        """
        need_count = True  # 在SparkSQL处理的时候是否最后执行.count()操作
        mc = self.main_construction
        if self.limit is not None:
            mc["LIMIT"] = [" ", str(self.limit), " "]

        mc = self.remove_orderby_if_exists(mc)
        if "GROUP BY" not in mc and "LIMIT" not in mc:
            mc["SELECT"] = [" ", "COUNT(*) AS cnt", " "]
            need_count = False

        return (self.print_main_construction(mc), need_count)

    def generate_execute_sql(self):
        """
        # 生成执行查询语句

        # 规则
        - 若原始SQL中存在`LIMIT`参数，且 `LIMIT` < `self.per_page_rows * self.page_number`，是第一页 => 查 `self.limit` 条
        - 若原始SQL中存在`LIMIT`参数，且 `LIMIT` >= `self.per_page_rows * self.page_number` => 查`self.per_page_rows * self.page_number`条
        - 若原始SQL中不存在`LIMIT`参数，查`self.per_page_rows * self.page_number`条 
        """
        limit = self.limit
        if limit is None or limit > self.per_page_rows * self.page_number:
            limit = self.per_page_rows * self.page_number

        mc = self.main_construction
        mc["LIMIT"] = [" ", str(limit), " "]
        return self.print_main_construction(mc)

    def get_pagination(self):
        start = (self.page_number - 1) * self.per_page_rows
        end = start + self.per_page_rows
        if self.limit is not None and self.limit < end:
            end = self.limit

        return (start, end)

    def remove_orderby_if_exists(self, main_construction):
        """若存在`ORDER BY`则删除"""
        if "ORDER BY" in main_construction:
            del main_construction["ORDER BY"]

        return main_construction

    def remove_semicolon_if_exists(self, main_construction):
        """删除分号"""
        if ";" in main_construction:
            del main_construction[";"]

        return main_construction

    def init_and_remove_limit_if_exists(self, main_construction):
        """从SQL获取分页参数LIMIT"""
        if "LIMIT" in main_construction:
            self.limit = int(
                "".join(main_construction.get("LIMIT")).strip())
            del main_construction["LIMIT"]

        return main_construction
