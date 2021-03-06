# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-30 17:55
from __future__ import unicode_literals

from django.db import migrations
import home.blocks
import wagtail.wagtailcore.blocks
import wagtail.wagtailcore.fields
import wagtail.wagtailimages.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0034_auto_20161230_1726'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dynamicpage',
            name='page_content',
            field=wagtail.wagtailcore.fields.StreamField((('subtitle', home.blocks.SubtitleBlock()), ('paragraph', wagtail.wagtailcore.blocks.StructBlock((('text_alignment', wagtail.wagtailcore.blocks.ChoiceBlock(choices=[('text-left', 'Links'), ('text-right', 'Rechts'), ('text-center', 'Centreer')], default='text-left', label='Tekst uitlijning')), ('text_width', wagtail.wagtailcore.blocks.IntegerBlock(default=12, help_text='Geeft de breedte van de paragraaf aan, waarbij 12 maximaal is. Som van tekst breedte en tekst offset is ook best maximaal 12', label='Tekst breedte', max_value=12, min_value=1)), ('text_offset', wagtail.wagtailcore.blocks.IntegerBlock(default=0, help_text='Geeft de offset van de paragraaf aan, dus hoever de paragraaf naar rechts wordt verschoven (0 = volledig links)', label='Tekst offset', max_value=10, min_value=0)), ('text', wagtail.wagtailcore.blocks.TextBlock(help_text='Plaats hier de tekst voor 1 paragraaf, en voeg zoveel paragrafen toe als nodig', label='Paragraaf tekst', min_length=160, required=False)), ('richtext', wagtail.wagtailcore.blocks.RichTextBlock(help_text="Deze wordt enkel getoond indien de 'Paragraaf tekst' leeg is", label='Richtext (= alternatief)', required=False))))), ('image', wagtail.wagtailcore.blocks.StructBlock(())), ('quote', wagtail.wagtailcore.blocks.StructBlock((('quote', wagtail.wagtailcore.blocks.CharBlock(help_text='Geef hier een citaat in', label='Citaat', max_length=164, required=True)),))), ('tabs', wagtail.wagtailcore.blocks.ListBlock(wagtail.wagtailcore.blocks.StructBlock((('tab_name', wagtail.wagtailcore.blocks.CharBlock(help_text='de titel voor het tabblad', label='tabblad titel', max_length=32, required=True)), ('rich_content', wagtail.wagtailcore.blocks.RichTextBlock(required=True)), ('text_width', wagtail.wagtailcore.blocks.IntegerBlock(default=12, help_text='Geeft de breedte van de tabs + inhoud aan, waarbij 12 maximaal is.', label='Breedte', max_value=12, min_value=1)))), icon='list-ul', template='home/blocks/tabbed_content_block.html')), ('video', home.blocks.BlogEmbedBlock()), ('slider', wagtail.wagtailcore.blocks.StructBlock((('afbeeldingen', wagtail.wagtailcore.blocks.ListBlock(wagtail.wagtailcore.blocks.StructBlock((('afbeelding', wagtail.wagtailimages.blocks.ImageChooserBlock()),)))), ('bijhorende_tekst', wagtail.wagtailcore.blocks.RichTextBlock()))))), null=True, verbose_name='pagina inhoud'),
        ),
    ]
