# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-30 17:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0033_auto_20161228_1937'),
    ]

    operations = [
        migrations.AlterField(
            model_name='homepagerecents',
            name='info',
            field=models.CharField(max_length=263, null=True, verbose_name='Titel tekst'),
        ),
    ]
