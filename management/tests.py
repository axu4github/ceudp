# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase, LiveServerTestCase
from management.models import User, Menu
from rest_framework.authtoken.models import Token
from django.core.exceptions import ObjectDoesNotExist


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
        change_list = [m9, m7, m10]
        u.menus.clear()  # 清除之前用户的所有菜单
        for m in change_list:
            u.menus.add(m)

        u_menus = u.menus.all()
        for m in change_list:
            self.assertTrue(m in u_menus)

        self.assertEqual(change_list.sort(), [item for item in u_menus].sort())
        self.assertTrue(m8 not in u_menus)
        self.assertEqual(
            "m9_修改后", u_menus.filter(name__startswith="m9")[0].name)


class RestFrameworkTokenAuthTest(LiveServerTestCase):
    """
    测试 django-rest-framework TokenAuthentication
    参考文档：
    - http://www.django-rest-framework.org/api-guide/authentication/#tokenauthentication
    - http://blog.csdn.net/lablenet/article/details/54667308
    """

    def test_generate_token(self):
        """测试创建Token"""
        u = User.objects.create_user(
            "token_user", "token_user@gmail.com", "token_user")
        # 生成用户 Token
        token = Token.objects.create(user=u)

        # 获取用户 Token
        t = Token.objects.get(user=u)

        self.assertEqual(token, t)

    def test_get_token(self):
        """测试获取或者创建用户Token"""
        u = User.objects.create_user("t2", "t2@gmail.com", "t2")
        try:
            token = Token.objects.get(user=u)
        except ObjectDoesNotExist:
            token = Token.objects.create(user=u)

        self.assertEqual(token, Token.objects.get(user=u))

    def test_user_get_or_create_token(self):
        """测试使用User.get_or_create_token()方法获取用户Token"""
        t3 = User.objects.create_user("t3", "t3@gmail.com", "t3")
        t3_token = t3.get_or_create_token()

        t4 = User.objects.create_user("t4", "t4@gmail.com", "t4")
        t4_token = t4.get_or_create_token()

        self.assertTrue(t3_token != t4_token)

    def test_token_to_user(self):
        """测试通过token返回用户信息"""
        t5 = User.objects.create_user("t5", "t5@gmail.com", "t5")
        token = t5.get_or_create_token()

        self.assertEqual(t5, Token.objects.get(key=token).user)


class MenuApisTest(LiveServerTestCase):
    """菜单的API接口测试"""

    def setUp(self):
        """初始化某个菜单为之后测试使用"""
        # self.urls = {
        #     "create": "/api/management/menus/",  # 创建接口
        # }

        # data = {
        #     "name": "api_m1",
        #     "code": "api_m1",
        # }

        # reponse = self.client.post(self.urls["create"], data)
        # print reponse
        pass

    def test_create(self):
        """创建菜单，POST请求测试"""
        pass

    def test_list(self):
        """获取菜单，GET请求测试"""
        pass

    def test_update(self):
        """全部更新菜单，PUT请求测试"""
        pass

    def test_delete(self):
        """删除菜单，DELETE请求测试"""
        pass

    def test_read_single(self):
        """读取单个菜单，GET带id请求测试"""
        pass

    def test_part_of_update(self):
        """部分更新菜单，PATCH请求测试"""
        pass
