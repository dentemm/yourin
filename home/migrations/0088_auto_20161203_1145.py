# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-12-03 11:45
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0087_auto_20161203_1136'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='aboutpage',
            name='catchphrase',
        ),
        migrations.RemoveField(
            model_name='blog',
            name='catchphrase',
        ),
        migrations.RemoveField(
            model_name='blogindex',
            name='catchphrase',
        ),
        migrations.RemoveField(
            model_name='calendarevent',
            name='catchphrase',
        ),
        migrations.RemoveField(
            model_name='calendarindex',
            name='catchphrase',
        ),
        migrations.RemoveField(
            model_name='calendarpage',
            name='catchphrase',
        ),
        migrations.RemoveField(
            model_name='contactpage',
            name='catchphrase',
        ),
        migrations.RemoveField(
            model_name='event',
            name='catchphrase',
        ),
        migrations.RemoveField(
            model_name='eventindex',
            name='catchphrase',
        ),
        migrations.RemoveField(
            model_name='influencer',
            name='catchphrase',
        ),
        migrations.RemoveField(
            model_name='influencerindex',
            name='catchphrase',
        ),
    ]
