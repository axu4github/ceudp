# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-12 21:41
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0008_alter_user_username_max_length'),
        ('management', '0010_customerpermission'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customerpermission',
            name='permission_ptr',
        ),
        migrations.DeleteModel(
            name='CustomerPermission',
        ),
    ]
