# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-15 10:30
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0016_auto_20170715_1002'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='custompermissions',
            options={'default_permissions': (), 'permissions': (('post:management_api:user-list', '\u7528\u6237\u521b\u5efa'), ('get:management_api:user-list', '\u7528\u6237\u5217\u8868\u67e5\u770b'), ('get:management_api:user-detail', '\u7528\u6237\u8be6\u60c5\u67e5\u770b'), ('get:management_api:user-menus', '\u7528\u6237\u83dc\u5355\u67e5\u770b'), ('get:management_api:user-enable', '\u7528\u6237\u542f\u7528'), ('get:management_api:user-disable', '\u7528\u6237\u7981\u7528'), ('put:management_api:user-detail', '\u7528\u6237\u4fe1\u606f\u4fee\u6539'), ('patch:management_api:user-detail', '\u7528\u6237\u4fe1\u606f\u90e8\u5206\u4fee\u6539'), ('post:management_api:user-change-password', '\u7528\u6237\u5bc6\u7801\u4fee\u6539'), ('post:performance_api:query-list', '\u67e5\u8be2'), ('get:performance_api:query-list', '\u67e5\u8be2\u5386\u53f2\u8bb0\u5f55\u67e5\u770b'), ('get:performance_api:query-detail', '\u67e5\u8be2\u5386\u53f2\u8bb0\u5f55\u8be6\u60c5\u67e5\u770b'), ('get:management_api:group-list', '\u7528\u6237\u7ec4\u5217\u8868\u67e5\u770b'), ('get:management_api:group-detail', '\u7528\u6237\u7ec4\u8be6\u60c5\u67e5\u770b'), ('get:management_api:permission-list', '\u6743\u9650\u5217\u8868\u67e5\u770b'))},
        ),
    ]