# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-22 19:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0045_remove_eventindex_name'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='event',
            options={'ordering': ['-event_date'], 'verbose_name': 'evenementen'},
        ),
        migrations.AlterField(
            model_name='event',
            name='name',
            field=models.CharField(default='', max_length=164, null=True, verbose_name='naam'),
        ),
    ]
