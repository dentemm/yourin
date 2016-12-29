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

	text_alignment = blocks.ChoiceBlock(label='Tekst uitlijning', choices=TEXT_ALIGNMENT_CHOICES)
	#text_alignment = blocks.CharBlock(label='Tekst uitlijning', max_length=16, choices=TEXT_ALIGNMENT_CHOICES, default='Links')
	text = blocks.TextBlock(label='Paragraaf tekst', min_length=160, required=True, help_text='Plaats hier de tekst voor 1 paragraaf, en voeg zoveel paragrafen toe als nodig')

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