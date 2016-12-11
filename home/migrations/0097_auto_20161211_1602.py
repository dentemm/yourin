# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-12-11 16:02
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0096_auto_20161209_1850'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='event',
            options={'verbose_name': 'event groep', 'verbose_name_plural': 'event groepen'},
        ),
        migrations.AlterModelOptions(
            name='eventinstance',
            options={'verbose_name': 'evenement', 'verbose_name_plural': 'evenementen'},
        ),
        migrations.AddField(
            model_name='eventinstance',
            name='website',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='image',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='home.CustomImage', verbose_name='afbeelding'),
        ),
    ]
