# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-12-15 18:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0006_auto_20161215_1828'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aboutpage',
            name='has_subtitle',
            field=models.BooleanField(default=True, verbose_name='Subtitel balk'),
        ),
        migrations.AlterField(
            model_name='blog',
            name='has_subtitle',
            field=models.BooleanField(default=True, verbose_name='Subtitel balk'),
        ),
        migrations.AlterField(
            model_name='blogindex',
            name='has_subtitle',
            field=models.BooleanField(default=True, verbose_name='Subtitel balk'),
        ),
        migrations.AlterField(
            model_name='calendarevent',
            name='has_subtitle',
            field=models.BooleanField(default=True, verbose_name='Subtitel balk'),
        ),
        migrations.AlterField(
            model_name='calendarindex',
            name='has_subtitle',
            field=models.BooleanField(default=True, verbose_name='Subtitel balk'),
        ),
        migrations.AlterField(
            model_name='calendarpage',
            name='has_subtitle',
            field=models.BooleanField(default=True, verbose_name='Subtitel balk'),
        ),
        migrations.AlterField(
            model_name='contactpage',
            name='has_subtitle',
            field=models.BooleanField(default=True, verbose_name='Subtitel balk'),
        ),
        migrations.AlterField(
            model_name='dynamicpage',
            name='has_subtitle',
            field=models.BooleanField(default=True, verbose_name='Subtitel balk'),
        ),
        migrations.AlterField(
            model_name='event',
            name='has_subtitle',
            field=models.BooleanField(default=True, verbose_name='Subtitel balk'),
        ),
        migrations.AlterField(
            model_name='eventindex',
            name='has_subtitle',
            field=models.BooleanField(default=True, verbose_name='Subtitel balk'),
        ),
        migrations.AlterField(
            model_name='homepage',
            name='has_subtitle',
            field=models.BooleanField(default=True, verbose_name='Subtitel balk'),
        ),
        migrations.AlterField(
            model_name='influencer',
            name='has_subtitle',
            field=models.BooleanField(default=True, verbose_name='Subtitel balk'),
        ),
        migrations.AlterField(
            model_name='influencerindex',
            name='has_subtitle',
            field=models.BooleanField(default=True, verbose_name='Subtitel balk'),
        ),
    ]