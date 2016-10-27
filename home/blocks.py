from wagtail.wagtailcore import blocks
from wagtail.wagtailimages.blocks import ImageChooserBlock
from wagtail.wagtailembeds.blocks import EmbedBlock

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

class ParagraphBlock(blocks.RichTextBlock):
	class Meta:
		template = 'home/blocks/paragraph_block.html'
		label = 'paragraaf'
		icon = 'edit'

class ImageWithCaptionBlock(blocks.StructBlock):
	class Meta:
		template = 'home/blocks/imagewithcaption_block.html'
		label = 'afbeelding met tekst'
		icon = 'image'

class PullQuoteBlock(blocks.StructBlock):
	class Meta:
		template = 'home/blocks/pullquote_block.html'
		label = 'citaat'
		icon = 'openquote'