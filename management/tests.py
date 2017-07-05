# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from management.models import User, Menu
from rest_framework.authtoken.models import Token
from django.core.exceptions import ObjectDoesNotExist
from errors import NoneUsernameOrPasswordError, UsernameOrPasswordIncorrectError, UserIsDisableError
from management.settings import settings
from management.authentications import Authentication
import json

__author__ = "axu"


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


class RestFrameworkTokenAuthTest(TestCase):
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

    def test_get_token_api(self):
        """测试通过API获取用户Token"""
        t6 = User.objects.create_user("t6", "t6@gmail.com", "t6")
        t6_token = t6.get_or_create_token().key

        reponse = self.client.post(
            "/api/management/login/", {"username": "t6", "password": "t6"})
        token = json.loads(reponse.content).get("token", None)

        self.assertEqual(t6_token, token)


class ErrorsTest(TestCase):
    """自定义错误测试"""

    def test_none_username_or_password_error(self):
        """测试没有发现用户或者密码错误"""
        error_message = ""
        try:
            raise NoneUsernameOrPasswordError()
        except NoneUsernameOrPasswordError as error:
            error_message = str(error)

        self.assertEqual(
            settings.ERROR_MESSAGES["NoneUsernameOrPasswordError"],
            error_message)

    def test_username_or_password_incorrect_error(self):
        """测试用户名或者密码错误"""
        error_message = ""
        try:
            raise UsernameOrPasswordIncorrectError()
        except UsernameOrPasswordIncorrectError as error:
            error_message = str(error)

        self.assertEqual(
            settings.ERROR_MESSAGES["UsernameOrPasswordIncorrectError"],
            error_message)

    def test_user_is_disable_error(self):
        """测试用户已经被禁用错误"""
        error_message = ""
        try:
            raise UserIsDisableError()
        except UserIsDisableError as error:
            error_message = str(error)

        self.assertEqual(
            settings.ERROR_MESSAGES["UserIsDisableError"],
            error_message)


class AuthenticationTest(TestCase):
    """自定义认证模块测试"""

    def setUp(self):
        self.auth_user = User.objects.create_user(
            "auth_user", "auth_user@gmail.com", "auth_user123")

    def test_correct_authenticate(self):
        """测试正确认证方法"""
        self.assertEqual(
            Authentication.authenticate("auth_user", "auth_user123"), self.auth_user)

    def test_none_username_or_password_error_authenticate(self):
        """测试没有发现用户或者密码错误"""
        error_message = ""
        try:
            Authentication.authenticate()
        except NoneUsernameOrPasswordError as error:
            error_message = str(error)

        self.assertEqual(
            settings.ERROR_MESSAGES["NoneUsernameOrPasswordError"],
            error_message)

    def test_username_or_password_incorrect_error_authenticate(self):
        """测试用户名或者密码错误"""
        error_message = ""
        try:
            Authentication.authenticate("auth_user", "auth_user")
        except UsernameOrPasswordIncorrectError as error:
            error_message = str(error)

        self.assertEqual(
            settings.ERROR_MESSAGES["UsernameOrPasswordIncorrectError"],
            error_message)

    def test_auth_403_error(self):
        """测试禁止访问"""
        response = self.client.get("/api/management/menus/")
        self.assertTrue(403, response.status_code)

    def test_correct_token_auth_from_api(self):
        """通过API进行正确的Token验证"""
        a = User.objects.create_user("auth_01", "auth_01@gmail.com", "auth_01")
        token = a.get_or_create_token().key

        response = self.client.get(
            "/api/management/menus/", HTTP_AUTHORIZATION="Token {token}".format(token=token))

        self.assertTrue(200, response.status_code)


class MenuApisTest(TestCase):
    """菜单的API接口测试"""

    def setUp(self):
        """初始化某个菜单为之后测试使用"""
        self.urls = {
            "create": "/api/management/menus/",  # 创建接口
            "list": "/api/management/menus/",  # 列表接口
            "detail": "/api/management/menus/{id}/",  # 详细信息接口
            "delete": "/api/management/menus/{id}/",  # 删除接口
            "update": "/api/management/menus/{id}/",  # 全部更新接口
            "part_of_update": "/api/management/menus/{id}/",  # 部分更新接口
        }

        self.user = User.objects.create_user(
            "menu_user", "menu_user@gmail.com", "menu_user")
        self.token = self.user.get_or_create_token().key
        self.ma = Menu.objects.create(name="ma", code="ma")
        self.user.menus.add(self.ma)
        self.user.save()

        self.other_user = User.objects.create_user(
            "menu_user_01", "menu_user_01@gmail.com", "menu_user_01")
        self.other_user_token = self.other_user.get_or_create_token().key

    def test_create_menu(self):
        """测试创建菜单，POST请求"""
        data = {
            "name": "ma1",
            "code": "ma1",
            "parent": self.ma.id,
            "linkto": "/ma1"
        }

        response = self.client.post(
            self.urls["create"], data, HTTP_AUTHORIZATION="Token " + self.token)
        response_content = json.loads(response.content)

        self.assertTrue(201, response.status_code)
        self.assertEqual(response_content.get("name"), data["name"])
        self.assertEqual(response_content.get("code"), data["code"])
        self.assertEqual(response_content.get("parent"), data["parent"])
        self.assertEqual(response_content.get("linkto"), data["linkto"])

    def test_list_menu(self):
        """测试获取菜单列表，GET请求"""
        response = self.client.get(
            self.urls["list"], HTTP_AUTHORIZATION="Token " + self.token)
        response_content = json.loads(response.content)

        self.assertEqual(200, response.status_code)
        self.assertTrue(len(response_content) > 0)

    def test_detail_menu(self):
        """测试获取菜单详细信息，GET请求"""
        response = self.client.get(
            self.urls["detail"].format(id=self.ma.id), HTTP_AUTHORIZATION="Token " + self.token)
        response_content = json.loads(response.content)

        self.assertEqual(200, response.status_code)
        self.assertEqual(response_content.get("name"), self.ma.name)
        self.assertEqual(response_content.get("code"), self.ma.code)
        self.assertEqual(response_content.get("parent"), 0)
        self.assertEqual(response_content.get("linkto"), self.ma.linkto)

    def test_update_menu(self):
        """测试更新菜单全部内容，PUT请求"""
        ma2 = Menu.objects.create(
            name="ma2", code="ma2", parent=self.ma, linkto="/ma2")

        # PUT请求的修改必须要填必填项，比如若想要修改ma2的linkto，则必须将name,code也一并传入，若只传入linkto则会报错。
        data = {
            "name": "ma2",
            "code": "ma2",
            "linkto": "/m2_updated"
        }

        json_data_str = json.dumps(data)

        # 注意：若content_type设置为application/json的话，data要传json字符串
        response = self.client.put(
            self.urls["update"].format(id=ma2.id), data=json_data_str,
            content_type="application/json",
            HTTP_AUTHORIZATION="Token " + self.token)
        response_content = json.loads(response.content)

        self.assertEqual(200, response.status_code)
        self.assertEqual(response_content.get("name"), data["name"])
        self.assertEqual(response_content.get("code"), data["code"])
        self.assertEqual(response_content.get("linkto"), data["linkto"])

    def test_part_of_update_menu(self):
        """测试更新菜单部分内容，PATCH请求"""
        m3 = Menu.objects.create(
            name="m3", code="m3", parent=self.ma, linkto="/m3")

        # PATCH请求的修改是不需要填必填项的，比如若想要修改ma3的linkto，则只需要传入linkto参数就可以完成修改，其他原有项内容不变。
        data = {"linkto": "/m3_updated"}
        json_data_str = json.dumps(data)

        # 注意：若content_type设置为application/json的话，data要传json字符串
        response = self.client.patch(
            self.urls["part_of_update"].format(id=m3.id), data=json_data_str,
            content_type="application/json",
            HTTP_AUTHORIZATION="Token " + self.token)
        response_content = json.loads(response.content)

        self.assertEqual(200, response.status_code)
        self.assertEqual(response_content.get("linkto"), data["linkto"])

    def test_delete_menu(self):
        """测试删除菜单，DELETE请求"""
        ma4 = Menu.objects.create(name="ma4", code="ma4")
        response = self.client.delete(
            self.urls["delete"].format(id=ma4.id), HTTP_AUTHORIZATION="Token " + self.token)

        self.assertEqual(204, response.status_code)
        self.assertEqual(0, len(Menu.objects.filter(name="ma4")))


class UserApisTest(TestCase):
    """用户接口测试"""

    def setUp(self):
        """测试数据准备"""
        pass

    def test_create_user(self):
        """测试创建用户接口"""
        pass

    def test_list_user(self):
        """测试浏览用户接口"""
        pass

    def test_detail_user(self):
        """测试浏览用户详情接口"""
        pass

    def test_update_user(self):
        """测试更新用户接口"""
        pass

    def test_part_of_update_user(self):
        """测试更新用户部分内容接口"""
        pass
