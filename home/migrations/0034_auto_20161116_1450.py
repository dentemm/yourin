# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-16 14:50
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0033_auto_20161115_1951'),
    ]

    operations = [
        migrations.CreateModel(
            name='WhatWeDo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40, verbose_name='naam')),
                ('extra_info', models.TextField(max_length=512, verbose_name='info tekst')),
                ('image', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='home.CustomImage', verbose_name='afbeelding')),
            ],
            options={
                'verbose_name': 'pijler',
                'verbose_name_plural': 'pijlers',
            },
        ),
        migrations.AlterModelOptions(
            name='homepage',
            options={'verbose_name': 'startpagina'},
        ),
    ]
