# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-24 09:18
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0060_auto_20161124_0900'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='HomePageNumbers',
            new_name='Numbers',
        ),
    ]
