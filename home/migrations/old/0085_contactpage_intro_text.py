# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-12-03 10:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0084_auto_20161203_1039'),
    ]

    operations = [
        migrations.AddField(
            model_name='contactpage',
            name='intro_text',
            field=models.CharField(default="'Vivamus sagittis lacus vel augue laoreet rutrum faucibus \n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\tdolor auctor. Cras justo odio, dapibus ac facilisis in, egestas \n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\teget quam. Cras mattis consectetur purus sit amet fermentum.", max_length=255),
        ),
    ]