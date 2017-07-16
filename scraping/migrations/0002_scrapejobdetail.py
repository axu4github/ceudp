# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-17 06:36
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('scraping', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ScrapeJobDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('execute_time', models.CharField(default='', max_length=50, verbose_name='\u6267\u884c\u65f6\u95f4')),
                ('content', models.CharField(default='', max_length=200, verbose_name='\u91c7\u96c6\u5185\u5bb9')),
                ('rows', models.IntegerField(verbose_name='\u91c7\u96c6\u6570\u91cf')),
                ('error_messages', models.TextField(default='', verbose_name='\u67e5\u8be2\u5185\u5bb9')),
                ('scrape_job', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scraping.ScrapeJob', verbose_name='\u91c7\u96c6\u4efb\u52a1')),
            ],
            options={
                'ordering': ('-created',),
            },
        ),
    ]
