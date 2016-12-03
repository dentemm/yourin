# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-29 08:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0072_auto_20161125_1841'),
    ]

    operations = [
        migrations.AddField(
            model_name='whatwedo',
            name='icon',
            field=models.CharField(choices=[('fa fa-bar-chart', 'Grafiek'), ('fa fa-car', 'Auto'), ('fa fa-battery-3', 'Batterij'), ('fa fa-bolt', 'Bliksem'), ('fa fa-bomb', 'Bom'), ('fa fa-calendar', 'kalender'), ('fa fa-camera', 'Fototoestel'), ('fa fa-child', 'Link'), ('fa fa-cloud', 'Wolk'), ('fa fa-commenting-o', 'Tekstballon'), ('fa fa-exclamation', 'Uitroepteken'), ('fa fa-flag', 'Vlag'), ('fa fa-gift', 'Geschenk'), ('fa fa-group', 'Groep mensen'), ('fa fa-glass', 'Glas'), ('fa fa-home', 'Home'), ('fa fa-heart-o', 'Hart'), ('fa fa-cutlery', 'Bestek'), ('fa fa-globe', 'Wereldbol'), ('fa fa-hashtag', 'Hashtag'), ('fa fa-key', 'Sleutel'), ('fa fa-magic', 'Toverstaf'), ('fa fa-microphone', 'Microfoon'), ('fa fa-mobile', 'GSM'), ('fa fa-paint-brush', 'Penceel'), ('fa fa-pencil', 'Potlood'), ('fa fa-quote-right', 'Aanhalingstekens'), ('fa fa-shopping-basket', 'Mandje'), ('fa fa-star', 'Ster'), ('fa fa-user', 'Gebruiker'), ('fa fa-video-camera', 'Camera')], default='fa fa-commenting-o', max_length=28),
        ),
        migrations.AlterField(
            model_name='numbers',
            name='icon',
            field=models.CharField(choices=[('fa fa-bar-chart', 'Grafiek'), ('fa fa-car', 'Auto'), ('fa fa-battery-3', 'Batterij'), ('fa fa-bolt', 'Bliksem'), ('fa fa-bomb', 'Bom'), ('fa fa-calendar', 'kalender'), ('fa fa-camera', 'Fototoestel'), ('fa fa-child', 'Link'), ('fa fa-cloud', 'Wolk'), ('fa fa-commenting-o', 'Tekstballon'), ('fa fa-exclamation', 'Uitroepteken'), ('fa fa-flag', 'Vlag'), ('fa fa-gift', 'Geschenk'), ('fa fa-group', 'Groep mensen'), ('fa fa-glass', 'Glas'), ('fa fa-home', 'Home'), ('fa fa-heart-o', 'Hart'), ('fa fa-cutlery', 'Bestek'), ('fa fa-globe', 'Wereldbol'), ('fa fa-hashtag', 'Hashtag'), ('fa fa-key', 'Sleutel'), ('fa fa-magic', 'Toverstaf'), ('fa fa-microphone', 'Microfoon'), ('fa fa-mobile', 'GSM'), ('fa fa-paint-brush', 'Penceel'), ('fa fa-pencil', 'Potlood'), ('fa fa-quote-right', 'Aanhalingstekens'), ('fa fa-shopping-basket', 'Mandje'), ('fa fa-star', 'Ster'), ('fa fa-user', 'Gebruiker'), ('fa fa-video-camera', 'Camera')], default='fa fa-bar-chart', max_length=28, verbose_name='icoon'),
        ),
        migrations.AlterField(
            model_name='whatwedo',
            name='extra_info',
            field=models.TextField(blank=True, max_length=180, null=True, verbose_name='info tekst'),
        ),
    ]