# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-12-03 10:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0082_contactlocation'),
    ]

    operations = [
        migrations.AddField(
            model_name='contactpage',
            name='email',
            field=models.EmailField(default='ditisde_emailvoor@contactformulier.website', max_length=254, verbose_name='contact email'),
        ),
    ]