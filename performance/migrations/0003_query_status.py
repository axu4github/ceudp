# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-19 16:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('performance', '0002_auto_20170617_0805'),
    ]

    operations = [
        migrations.AddField(
            model_name='query',
            name='status',
            field=models.CharField(choices=[(0, 'success'), (-1, 'failed')], default=-1, max_length=10, verbose_name='\u67e5\u8be2\u72b6\u6001'),
        ),
    ]
