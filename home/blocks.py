from django import forms

from wagtail.wagtailcore import blocks
from wagtail.wagtailimages.blocks import ImageChooserBlock
from wagtail.wagtailembeds.blocks import EmbedBlock

TEXT_ALIGNMENT_CHOICES = (
	('text-left', 'Links'),
	('text-right', 'Rechts'),
	('text-center', 'Centreer'),
)

class CarouselImageBlock(blocks.StructBlock):

	afbeelding = ImageChooserBlock()
	#tekst = blocks.CharBlock(required=False)

	class Meta:
		icon = 'image'
		label = 'carousel afbeelding'

class BlogTitleBlock(blocks.StructBlock):

	image = ImageChooserBlock(label='afbeelding', required=True)
	title = blocks.CharBlock(label='titel', required=True)

	class Meta:
		template = 'home/blocks/title_block.html'
		label =	'titel' 
		icon = 'title'

class SubtitleBlock(blocks.CharBlock):
	class Meta:
		template = 'home/blocks/subtitle_block.html'
		label = 'ondertitel'
		icon = 'pilcrow'

class IntroTextBlock(blocks.TextBlock):
	class Meta:
		template = 'home/blocks/introtext_block.html'
		label = 'intro'
		icon = 'snippet'



class ParagraphBlock(blocks.StructBlock):

	text_alignment = blocks.ChoiceBlock(label='Tekst uitlijning', choices=TEXT_ALIGNMENT_CHOICES, default='text-left')
	text_width = blocks.IntegerBlock(label='Tekst breedte',default=12, min_value=1, max_value=12, help_text="Geeft de breedte van de paragraaf aan, waarbij 12 maximaal is. Som van tekst breedte en tekst offset is ook best maximaal 12")
	text_offset = blocks.IntegerBlock(label='Tekst offset', default=0, min_value=0, max_value=10, help_text="Geeft de offset van de paragraaf aan, dus hoever de paragraaf naar rechts wordt verschoven (0 = volledig links)")
	text = blocks.TextBlock(label='Paragraaf tekst', min_length=160, required=False, help_text='Plaats hier de tekst voor 1 paragraaf, en voeg zoveel paragrafen toe als nodig')
	richtext = blocks.RichTextBlock(label='Richtext (= alternatief)', required=False, help_text="Deze wordt enkel getoond indien de 'Paragraaf tekst' leeg is")

	class Meta:
		template = 'home/blocks/paragraph_block.html'
		label = 'paragraaf'
		icon = 'edit'

class BlogEmbedBlock(blocks.URLBlock):

	class Meta:
		template = 'home/blocks/embed_block.html'
		label = 'video embed'
		icon = 'media'

class ImageWithCaptionBlock(blocks.StructBlock):
	class Meta:
		template = 'home/blocks/imagewithcaption_block.html'
		label = 'afbeelding met tekst'
		icon = 'image'

class PullQuoteBlock(blocks.StructBlock):

	quote = blocks.CharBlock(label='Citaat', required=True, max_length=164, help_text='Geef hier een citaat in')

	class Meta:
		template = 'home/blocks/pullquote_block.html'
		label = 'citaat'
		icon = 'openquote'

#('slider', ListBlock(customblocks.CarouselImageBlock(), template='home/blocks/carousel_block.html', icon='image')),

class SliderBlock(blocks.StructBlock):

	afbeeldingen = blocks.ListBlock(CarouselImageBlock())
	bijhorende_tekst = blocks.RichTextBlock()

	class Meta:
		template = 'home/blocks/slider_block.html'
		label = 'slider'
		icon = 'image'


class TabbedContentItem(blocks.StructBlock):

	tab_name = blocks.CharBlock(label='tabblad titel', required=True, max_length=32, help_text='de titel voor het tabblad')
	rich_content = blocks.RichTextBlock(required=True)
	text_width = blocks.IntegerBlock(label='Breedte',default=12, min_value=1, max_value=12, help_text="Geeft de breedte van de tabs + inhoud aan, waarbij 12 maximaal is.")


class TwoColsBlock(blocks.StructBlock):

	#left = blocks.RichTextBlock(label='linkse kolom', required=True)
	#right = blocks.RichTextBlock(label='rechtse kolom', required=True)

	content = blocks.StreamBlock([
		('linkse_kolom', blocks.RichTextBlock()),
		('rechtse_kolom', blocks.RichTextBlock()),

		], icon='arrow-left', label='inhoud')


	# left = blocks.StreamBlock([
	# 	('linkse_kolom', blocks.RichTextBlock()),

	# 	], icon='arrow-left', label='inhoud')

	# right = blocks.StreamBlock([
	# 	('rechtse_kolom', blocks.RichTextBlock()),
		
	# 	], icon='arrow-right', label='inhoud')

	class Meta:	
		template = 'home/blocks/two_cols.html'
		icon = 'placeholder'
		label = '2 kolommen'
		form_classname = 'range'