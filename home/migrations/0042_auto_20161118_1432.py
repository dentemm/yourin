# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-18 14:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0041_auto_20161118_1419'),
    ]

    operations = [
        migrations.AlterField(
            model_name='influencer',
            name='name',
            field=models.CharField(max_length=128, null=True),
        ),
    ]
