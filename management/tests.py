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

    def test_delete_menu(self):
        """测试删除菜单"""
        m5 = Menu.objects.create(name="m5", code="m5")
        self.user.menus.add(m5)
        self.assertTrue(m5 in self.user.menus.all())

        m5.delete()
        self.assertTrue(m5 not in self.user.menus.all())

    def test_update_menu(self):
        """测试更改菜单"""
        m6 = Menu.objects.create(name="m6", code="m6")
        self.user.menus.add(m6)
        self.assertEqual(
            "m6", self.user.menus.filter(name__startswith="m6")[0].name)

        m6.name = "m6_修改后"
        m6.save()
        self.assertEqual(
            "m6_修改后", self.user.menus.filter(name__startswith="m6")[0].name)

    def test_update_menu_list(self):
        """测试修改菜单列"""
        u = User.objects.create_user("u", "u@gmail.com", "u")
        m7 = Menu.objects.create(name="m7", code="m7")
        m8 = Menu.objects.create(name="m8", code="m8")
        m9 = Menu.objects.create(name="m9", code="m9")
        add_list = [m7, m8, m9]
        # self.user.menus.add(m7, m8, m9)
        for m in add_list:
            u.menus.add(m)

        u_menus = u.menus.all()
        for m in add_list:
            self.assertTrue(m in u_menus)

        m9.name = "m9_修改后"
        m9.save()
        m10 = Menu.objects.create(name="m10", code="m10")
        # 在这里因为原来的菜单列表为[m7, m8, m9]，所以需要添加的为"m10"，需要删除的为"m8"。
        change_list = [m7, m9, m10]
        u.menus.clear()  # 清除之前用户的所有菜单
        for m in change_list:
            u.menus.add(m)

        u_menus = u.menus.all()
        for m in change_list:
            self.assertTrue(m in u_menus)

        self.assertTrue(not m8 in u_menus)
        self.assertEqual(
            "m9_修改后", u_menus.filter(name__startswith="m9")[0].name)
