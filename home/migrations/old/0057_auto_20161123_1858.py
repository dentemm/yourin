# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-23 18:58
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0056_homepagecontent'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='homepagecontent',
            name='page',
        ),
        migrations.RemoveField(
            model_name='whatwedo',
            name='image',
        ),
        migrations.RemoveField(
            model_name='whatwedo',
            name='related_page',
        ),
        migrations.DeleteModel(
            name='HomePageContent',
        ),
        migrations.DeleteModel(
            name='WhatWeDo',
        ),
    ]