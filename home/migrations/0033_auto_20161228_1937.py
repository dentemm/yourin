# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-28 19:37
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0032_homepagerecents_info'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='influencer',
            options={'ordering': ['-num_followers'], 'verbose_name': 'influencer', 'verbose_name_plural': 'influencers'},
        ),
    ]
