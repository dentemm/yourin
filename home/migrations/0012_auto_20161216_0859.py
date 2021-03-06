# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-16 08:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0011_event_intro'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customrendition',
            name='filter_spec',
            field=models.CharField(db_index=True, max_length=255),
        ),
        migrations.AlterUniqueTogether(
            name='customrendition',
            unique_together=set([('image', 'filter_spec', 'focal_point_key')]),
        ),
    ]
