# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from management.models import User, Menu


class MenuTablesTest(TestCase):
    """菜单表的单元测试"""

    def setUp(self):
        # 首先创建一条记录，为了之后测试修改，查询，删除使用
        self.user = User.objects.create_user(
            "test_menuer", "test_menuer@gmail.com", "test_menuer")
        self.root = Menu.objects.create(name="主节点", code="root")
        self.user.menus.add(self.root)
        self.user.save()

    def test_created_user_menus(self):
        """测试已创建的用户菜单"""
        user_first_menu = User.objects.filter(
            username="test_menuer")[0].menus.all()[0]
        self.assertEqual("主节点", user_first_menu.name)
        self.assertEqual("root", user_first_menu.code)

    def test_get_top_level_menu(self):
        """测试获取所有顶级菜单"""
        self.assertTrue(self.root in Menu.objects.filter(parent=0))

    def test_create_menu(self):
        """测试创建菜单"""
        f = Menu(name="第一个子节点", code="first_leaf_menu")
        f.parent = self.root
        f.save()

        self.assertEqual("第一个子节点", f.name)
        self.assertEqual("first_leaf_menu", f.code)
        self.assertTrue(f.is_leaf)
        self.assertEqual(self.root, f.parent)
        self.assertEqual("#", f.linkto)

    def test_auto_add_isleaf_by_save(self):
        """使用save()方式测试自动添加is_leaf方法"""
        m1 = Menu(name="m1", code="m1")
        m1.save()
        self.assertTrue(not m1.is_leaf)

        m2 = Menu(name="m2", code="m2", parent=self.root)
        m2.save()
        self.assertTrue(m2.is_leaf)

    def test_auto_add_isleaf_by_create(self):
        """使用create()方式测试自动添加is_leaf方法"""
        m3 = Menu.objects.create(name="m3", code="m3")
        self.assertTrue(not m3.is_leaf)

        m4 = Menu.objects.create(name="m4", code="m4", parent=self.root)
        self.assertTrue(m4.is_leaf)
