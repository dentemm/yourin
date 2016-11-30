# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-30 11:13
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import modelcluster.fields


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0080_address_location'),
    ]

    operations = [
        migrations.CreateModel(
            name='EventLocation',
            fields=[
                ('location_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='home.Location')),
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('page', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='locations', to='home.Event')),
            ],
            options={
                'abstract': False,
                'ordering': ['sort_order'],
            },
            bases=('home.location', models.Model),
        ),
    ]
