# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from management.models import User, Menu


class MenuTablesTest(TestCase):
    """菜单表的单元测试"""

    def setUp(self):
        # 首先创建一条记录，为了之后测试修改，查询，删除使用
        user = User.objects.create_user(
            "test_menuer", "test_menuer@gmail.com", "test_menuer")
        menu = Menu.objects.create(name="主节点", code="root")
        user.menus.add(menu)
        user.save()

    def test_users_menu(self):
        user_first_menu = User.objects.filter(
            username="test_menuer")[0].menus.all()[0]
        self.assertEqual("主节点", user_first_menu.name)
        self.assertEqual("root", user_first_menu.code)
