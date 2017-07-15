# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
from django.test import TestCase
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission
from management.models import User
from security.models import AuditLog, ACTION

__author__ = "axu"


class AuditLogTableTest(TestCase):
    """审计日志表单元测试"""

    def test_create(self):
        alt01 = User.objects.create_user(
            "alt01", "alt01@gmail.com", "alt01")

        ct_user = ContentType.objects.get(model="user")
        al01 = AuditLog.objects.create(
            user=alt01, content_type=ct_user, action=ACTION.CREATE, content="{'alt01'}")

        self.assertEqual(al01.user, alt01)
        self.assertEqual(al01.content_type, ct_user)
        self.assertEqual(al01.action, ACTION.CREATE)
        self.assertEqual(al01.content, "{'alt01'}")


class AuditLogAPITest(TestCase):
    """审计日志API测试"""

    def setUp(self):
        self.urls = {
            "create": "/api/management/users/",  # 创建接口
            "list": "/api/management/users/",  # 列表接口
            "update": "/api/management/users/{id}/",  # 全部更新接口
            "part_of_update": "/api/management/users/{id}/",  # 部分更新接口
            "list_auditlog": "/api/security/auditlogs/",  # 审计日志列表接口
        }

        self.ala = User.objects.create_user("ala", "ala@gmail.com", "ala")
        put_permission = Permission.objects.get(
            codename="put:management_api:user-detail")
        patch_permission = Permission.objects.get(
            codename="patch:management_api:user-detail")
        create_permission = Permission.objects.get(
            codename="post:management_api:user-list")
        list_auditlog_permission = Permission.objects.get(
            codename="get:security_api:auditlog-list")
        self.ala.user_permissions.add(
            put_permission,
            patch_permission,
            create_permission,
            list_auditlog_permission
        )
        self.ala_token = self.ala.get_or_create_token().key

    def test_create_from_api(self):
        data = {
            "username": "ala01",
            "email": "ala01@gmail.com"
        }

        self.client.post(
            self.urls["create"], data, HTTP_AUTHORIZATION="Token " + self.ala_token)

        ct_user = ContentType.objects.get(model="user")
        als = AuditLog.objects.filter(
            content_type=ct_user, action=ACTION.CREATE)

        self.assertEqual(als[0].user, self.ala)

    def test_update_from_api(self):
        ala02 = User.objects.create_user("ala02", "ala02@gmail.com", "ala02")
        data = {
            "username": "ala02",
            "email": "ala02_uploaded@gmail.com",
        }

        json_data_str = json.dumps(data)

        # 注意：若content_type设置为application/json的话，data要传json字符串
        self.client.put(
            self.urls["update"].format(id=ala02.id), data=json_data_str,
            content_type="application/json",
            HTTP_AUTHORIZATION="Token " + self.ala_token)

        als = AuditLog.objects.filter(action=ACTION.UPDATE)

        self.assertEqual(als[0].user, self.ala)

    def test_patch_from_api(self):
        ala03 = User.objects.create_user("ala03", "ala03@gmail.com", "ala03")
        data = {
            "email": "ala03_uploaded@gmail.com",
        }

        json_data_str = json.dumps(data)

        # 注意：若content_type设置为application/json的话，data要传json字符串
        self.client.patch(
            self.urls["part_of_update"].format(id=ala03.id), data=json_data_str,
            content_type="application/json",
            HTTP_AUTHORIZATION="Token " + self.ala_token)

        als = AuditLog.objects.filter(action=ACTION.UPDATE)

        self.assertEqual(als[0].user, self.ala)

    def test_list_from_api(self):
        data = {
            "username": "ala04",
            "email": "ala04@gmail.com"
        }

        self.client.post(
            self.urls["create"], data, HTTP_AUTHORIZATION="Token " + self.ala_token)

        response = self.client.get(
            self.urls["list_auditlog"], HTTP_AUTHORIZATION="Token " + self.ala_token)
        response_content = json.loads(response.content)

        self.assertEqual(200, response.status_code)
        self.assertTrue(len(response_content) > 0)
