# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-25 18:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0071_auto_20161125_1838'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='category',
            field=models.PositiveIntegerField(choices=[(1, 'Sport'), (2, 'Kamp'), (3, 'Festival'), (4, 'Club')], default=1),
        ),
    ]
