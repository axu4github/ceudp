# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-24 22:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('performance', '0007_query_page_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='query',
            name='page_number',
            field=models.IntegerField(default=1, verbose_name='\u9875\u6570'),
        ),
    ]
