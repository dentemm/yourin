# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-24 15:58
from __future__ import unicode_literals

from django.db import migrations
import home.blocks
import wagtail.wagtailcore.blocks
import wagtail.wagtailcore.fields
import wagtail.wagtailembeds.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0064_auto_20161124_1541'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='blog_content',
            field=wagtail.wagtailcore.fields.StreamField((('blog_paragraph', home.blocks.ParagraphBlock()), ('blog_image', wagtail.wagtailcore.blocks.StructBlock(())), ('blog_quote', wagtail.wagtailcore.blocks.StructBlock((('quote', wagtail.wagtailcore.blocks.CharBlock(help_text='Geef hier een citaat in', label='Citaat', max_length=164, required=True)),))), ('blog_video', wagtail.wagtailembeds.blocks.EmbedBlock())), verbose_name='Blog Inhoud'),
        ),
    ]
