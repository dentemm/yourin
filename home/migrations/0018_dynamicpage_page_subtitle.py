# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-19 19:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0017_auto_20161218_1838'),
    ]

    operations = [
        migrations.AddField(
            model_name='dynamicpage',
            name='page_subtitle',
            field=models.CharField(blank=True, max_length=36, null=True, verbose_name='ondertitel'),
        ),
    ]
