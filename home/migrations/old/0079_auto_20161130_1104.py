# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-30 11:04
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0078_auto_20161130_1057'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='eventlocation',
            name='location_ptr',
        ),
        migrations.RemoveField(
            model_name='eventlocation',
            name='page',
        ),
        migrations.RemoveField(
            model_name='location',
            name='address',
        ),
        migrations.DeleteModel(
            name='Address',
        ),
        migrations.DeleteModel(
            name='EventLocation',
        ),
        migrations.DeleteModel(
            name='Location',
        ),
    ]