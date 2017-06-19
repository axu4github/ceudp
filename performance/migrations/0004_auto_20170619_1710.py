# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-19 17:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('performance', '0003_query_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='query',
            name='status',
            field=models.CharField(choices=[(0, 'success'), (-1, 'failed')], default=-1, max_length=2, verbose_name='\u67e5\u8be2\u72b6\u6001'),
        ),
    ]