# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-12-08 15:55
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0091_auto_20161208_1543'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='eventgroup',
            name='event_date',
        ),
        migrations.RemoveField(
            model_name='eventgroup',
            name='event_duration',
        ),
    ]
