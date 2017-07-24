# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
# from scraping.models import ScrapeJob
from datetime import datetime, timedelta


class ScrapeJobTableTest(TestCase):
    """采集任务表测试（需要补充）"""

    def test_datetime(self):
        now = datetime.now()
        next_time = datetime.now() + timedelta(seconds=10)

        self.assertFalse(now >= next_time)
        self.assertTrue(now <= next_time)

    def test_scrape_job_run(self):
        # sj = ScrapeJob.objects.create(
        #     job_name="Job-01",
        #     job_type="FILE",
        #     data_source="/path",
        #     destination="table-01",
        #     interval="20",
        #     next_time=datetime.now() + timedelta(seconds=20))

        # sj.run()

        # print sj.status
        # print sj.pid
        pass


class ScrapeJobAPITest(TestCase):
    """采集任务API测试（需要补充）"""
    pass


class ScrapeJobAPIPermissionTest(TestCase):
    """采集任务API权限测试（需要补充）"""
    pass


class ScrapeJobDetailTableTest(TestCase):
    """采集任务详情

    表测试（需要补充）"""
    pass


class ScrapeJobDetailAPITest(TestCase):
    """采集任务详情API测试（需要补充）"""
    pass


class ScrapeJobDetailAPIPermissionTest(TestCase):
    """采集任务详情API权限测试（需要补充）"""
    pass
