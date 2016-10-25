from wagtail.wagtailcore import blocks
from wagtail.wagtailimages.blocks import ImageChooserBlock
from wagtail.wagtailembeds.blocks import EmbedBlock

class TitleBlock(blocks.StructBlock):
	pass

class SubtitleBlock(blocks.CharBlock):
	pass

class IntroTextBlock(blocks.TextBlock):
	pass

class ParagraphBlock(blocks.RichTextBlock):
	pass 

class ImageWithCaptionBlock(blocks.StructBlock):
	pass

class PullQuoteBlock(blocks.StructBlock):
	pass