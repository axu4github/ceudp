# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-15 03:03
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('performance', '0008_auto_20170624_2226'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='query',
            options={'default_permissions': (), 'ordering': ('-created',), 'permissions': (('post:performance_api:query-list', '\u67e5\u8be2'), ('get:performance_api:query-list', '\u67e5\u8be2\u5386\u53f2\u8bb0\u5f55\u67e5\u770b'), ('get:performance_api:query-detail', '\u67e5\u8be2\u5386\u53f2\u8bb0\u5f55\u8be6\u60c5\u67e5\u770b'))},
        ),
    ]