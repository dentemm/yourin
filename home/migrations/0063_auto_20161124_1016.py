# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-24 10:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0062_auto_20161124_0941'),
    ]

    operations = [
        migrations.AlterField(
            model_name='numbers',
            name='value',
            field=models.PositiveIntegerField(default=1, verbose_name='cijfer'),
        ),
    ]
