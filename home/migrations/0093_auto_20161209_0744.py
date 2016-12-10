# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-12-09 07:44
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0030_index_on_pagerevision_created_at'),
        ('wagtailredirects', '0005_capitalizeverbose'),
        ('wagtailforms', '0003_capitalizeverbose'),
        ('home', '0092_eventeventinstance'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='eventgroup',
            name='image',
        ),
        migrations.RemoveField(
            model_name='eventgroup',
            name='page_ptr',
        ),
        migrations.RemoveField(
            model_name='eventgroup',
            name='tags',
        ),
        migrations.DeleteModel(
            name='EventGroup',
        ),
    ]