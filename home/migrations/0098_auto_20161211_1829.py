# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-12-11 18:29
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0097_auto_20161211_1602'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='eventinstance',
            options={'ordering': ['-event_date', 'event_name'], 'verbose_name': 'evenement', 'verbose_name_plural': 'evenementen'},
        ),
    ]
