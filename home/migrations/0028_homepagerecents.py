# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-28 17:33
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import modelcluster.fields


class Migration(migrations.Migration):

    dependencies = [
        #('wagtailcore', '0034_auto_20161227_1937'),
        ('home', '0027_eventinstancepagelocation'),
    ]

    operations = [
        migrations.CreateModel(
            name='HomePageRecents',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('button_text', models.CharField(default='Meer info', max_length=28, verbose_name='Link tekst')),
                ('page', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='recents', to='home.HomePage')),
                ('related_page', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailcore.Page', verbose_name='Link naar pagina')),
            ],
            options={
                'ordering': ['sort_order'],
                'abstract': False,
            },
        ),
    ]
