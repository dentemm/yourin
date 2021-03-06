# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-18 09:56
from __future__ import unicode_literals

from django.db import migrations
import home.blocks
import wagtail.wagtailcore.blocks
import wagtail.wagtailcore.fields
import wagtail.wagtailimages.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0015_auto_20161218_0956'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dynamicpage',
            name='page_content',
            field=wagtail.wagtailcore.fields.StreamField((('subtitle', home.blocks.SubtitleBlock()), ('paragraph', home.blocks.ParagraphBlock()), ('image', wagtail.wagtailcore.blocks.StructBlock(())), ('quote', wagtail.wagtailcore.blocks.StructBlock((('quote', wagtail.wagtailcore.blocks.CharBlock(help_text='Geef hier een citaat in', label='Citaat', max_length=164, required=True)),))), ('tabs', wagtail.wagtailcore.blocks.ListBlock(wagtail.wagtailcore.blocks.StructBlock((('tab_name', wagtail.wagtailcore.blocks.CharBlock(help_text='de titel voor het tabblad', label='tabblad titel', max_length=32, required=True)), ('content', wagtail.wagtailcore.blocks.TextBlock()))), icon='list-ul', template='home/blocks/tabbed_content_block.html')), ('video', home.blocks.BlogEmbedBlock()), ('two_cols', wagtail.wagtailcore.blocks.StructBlock((('content', wagtail.wagtailcore.blocks.StreamBlock((('linkse_kolom', wagtail.wagtailcore.blocks.RichTextBlock()), ('rechtse_kolom', wagtail.wagtailcore.blocks.RichTextBlock())), icon='arrow-left', label='inhoud')),), classname='range')), ('slider', wagtail.wagtailcore.blocks.ListBlock(wagtail.wagtailcore.blocks.StructBlock((('afbeelding', wagtail.wagtailimages.blocks.ImageChooserBlock()), ('tekst', wagtail.wagtailcore.blocks.CharBlock(required=False)))), icon='image', template='home/blocks/carousel.html'))), null=True, verbose_name='pagina inhoud'),
        ),
    ]
