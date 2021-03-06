# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-18 08:50
from __future__ import unicode_literals

from django.db import migrations, models
import home.blocks
import wagtail.wagtailcore.blocks
import wagtail.wagtailcore.fields


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0012_auto_20161216_0859'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dynamicpage',
            name='page_content',
            field=wagtail.wagtailcore.fields.StreamField((('subtitle', home.blocks.SubtitleBlock()), ('paragraph', home.blocks.ParagraphBlock()), ('image', wagtail.wagtailcore.blocks.StructBlock(())), ('quote', wagtail.wagtailcore.blocks.StructBlock((('quote', wagtail.wagtailcore.blocks.CharBlock(help_text='Geef hier een citaat in', label='Citaat', max_length=164, required=True)),))), ('tabs', wagtail.wagtailcore.blocks.ListBlock(wagtail.wagtailcore.blocks.StructBlock((('tab_name', wagtail.wagtailcore.blocks.CharBlock(help_text='de titel voor het tabblad', label='tabblad titel', max_length=32, required=True)), ('content', wagtail.wagtailcore.blocks.TextBlock()))), icol='list-ul', template='home/blocks/tabbed_content_block.html')), ('video', home.blocks.BlogEmbedBlock()), ('two_cols', wagtail.wagtailcore.blocks.StructBlock((('left', wagtail.wagtailcore.blocks.StreamBlock((('subtitel', home.blocks.SubtitleBlock()),), icon='arrow-left', label='Linkse kolom')), ('right', wagtail.wagtailcore.blocks.StreamBlock((('subtitel', home.blocks.SubtitleBlock()),), icon='arrow-right', label='Rechtse kolom'))), classname='range'))), null=True, verbose_name='pagina inhoud'),
        ),
        migrations.AlterField(
            model_name='influencer',
            name='name',
            field=models.CharField(max_length=128, null=True),
        ),
    ]
