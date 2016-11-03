# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-01 10:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0011_auto_20161101_1014'),
    ]

    operations = [
        migrations.CreateModel(
            name='NewsCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
            ],
            options={
                'ordering': ['name'],
                'verbose_name': 'Nieuwscategorie',
                'verbose_name_plural': 'Nieuwscategorieën',
            },
        ),
        migrations.RenameModel(
            old_name='Category',
            new_name='EventCategory',
        ),
        migrations.AlterModelOptions(
            name='eventcategory',
            options={'ordering': ['name'], 'verbose_name': 'Evenement Categorie', 'verbose_name_plural': 'Evenement Categorieën'},
        ),
    ]