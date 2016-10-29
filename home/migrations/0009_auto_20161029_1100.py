# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-29 11:00
from __future__ import unicode_literals

import datetime
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import home.models


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailforms', '0003_capitalizeverbose'),
        ('wagtailimages', '0015_fill_filter_spec_field'),
        ('wagtailcore', '0030_index_on_pagerevision_created_at'),
        ('wagtailredirects', '0005_capitalizeverbose'),
        ('home', '0008_auto_20161029_0853'),
    ]

    operations = [
        migrations.CreateModel(
            name='CalendarEvent',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('name', models.CharField(max_length=164, verbose_name='naam')),
                ('description', models.TextField(verbose_name='beschrijving')),
                ('event_date', models.DateField(default=datetime.date.today, verbose_name='datum')),
                ('event_duration', models.PositiveIntegerField(default=1, validators=[django.core.validators.MaxValueValidator(21)], verbose_name='Duur (# dagen)')),
                ('website', models.URLField(verbose_name='event website')),
                ('image', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.Image')),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='CalendarIndex',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.RemoveField(
            model_name='calenderevent',
            name='page_ptr',
        ),
        migrations.AlterField(
            model_name='customimage',
            name='file',
            field=models.ImageField(height_field='height', upload_to=home.models.get_upload_to, validators=[home.models.validate_image_min], verbose_name='file', width_field='width'),
        ),
        migrations.DeleteModel(
            name='CalenderEvent',
        ),
    ]