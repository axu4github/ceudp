# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-03 21:09
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0002_menu'),
    ]

    operations = [
        migrations.RenameField(
            model_name='menu',
            old_name='user',
            new_name='users',
        ),
    ]