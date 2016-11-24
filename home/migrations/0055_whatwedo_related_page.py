# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-23 18:25
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0030_index_on_pagerevision_created_at'),
        ('home', '0054_auto_20161123_1430'),
    ]

    operations = [
        migrations.AddField(
            model_name='whatwedo',
            name='related_page',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailcore.Page', verbose_name='Link naar pagina'),
        ),
    ]