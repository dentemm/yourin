# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-28 19:12
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0030_index_on_pagerevision_created_at'),
        ('home', '0005_auto_20161028_1523'),
    ]

    operations = [
        migrations.CreateModel(
            name='BlogIndex',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.AlterModelOptions(
            name='address',
            options={'ordering': ['city'], 'verbose_name': 'adres', 'verbose_name_plural': 'adressen'},
        ),
        migrations.AlterModelOptions(
            name='location',
            options={'ordering': ['name'], 'verbose_name': 'locatie', 'verbose_name_plural': 'locaties'},
        ),
        migrations.AddField(
            model_name='blog',
            name='intro_text',
            field=models.TextField(default='', verbose_name='intro text'),
        ),
        migrations.AddField(
            model_name='blog',
            name='name',
            field=models.CharField(default='', max_length=128, verbose_name='blog titel'),
        ),
        migrations.AddField(
            model_name='newsarticle',
            name='pub_date',
            field=models.DateField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='newsarticle',
            name='update_date',
            field=models.DateField(auto_now=True, null=True),
        ),
    ]