# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-04 19:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0035_auto_20161230_1755'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='blog',
            options={'ordering': ['-date'], 'verbose_name': 'blog artikel', 'verbose_name_plural': 'blog artikels'},
        ),
        migrations.RemoveField(
            model_name='contactpage',
            name='has_subtitle',
        ),
        migrations.AddField(
            model_name='contactpage',
            name='from_address',
            field=models.CharField(blank=True, max_length=255, verbose_name='from address'),
        ),
        migrations.AddField(
            model_name='contactpage',
            name='subject',
            field=models.CharField(blank=True, max_length=255, verbose_name='subject'),
        ),
        migrations.AddField(
            model_name='contactpage',
            name='to_address',
            field=models.CharField(blank=True, help_text='Optional - form submissions will be emailed to these addresses. Separate multiple addresses by comma.', max_length=255, verbose_name='to address'),
        ),
    ]
