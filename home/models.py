from __future__ import absolute_import, unicode_literals

import geopy	# to geocode location data
from datetime import date

from django.db import models as djangomodels
from django.core.validators import MinValueValidator, MaxValueValidator

from wagtail.wagtailcore.models import Page, Orderable
from wagtail.wagtailcore import fields
from wagtail.wagtailadmin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel, FieldRowPanel, StreamFieldPanel
from wagtail.wagtailsnippets.models import register_snippet

from django_countries.fields import CountryField

from .blocks import BlogTitleBlock, SubtitleBlock, IntroTextBlock, ParagraphBlock, ImageWithCaptionBlock, PullQuoteBlock

@register_snippet
class Location(djangomodels.Model):

	name = djangomodels.CharField(max_length=64)
	address = djangomodels.ForeignKey('home.Address', verbose_name='adres', related_name='location', null=True)
	longitude = djangomodels.DecimalField(max_digits=10, decimal_places=7, blank=True, null=True)
	latitude = djangomodels.DecimalField(max_digits=10, decimal_places=7, blank=True, null=True)

	class Meta:
		verbose_name = 'locatie'
		verbose_name_plural = 'locaties'
		ordering = ['name', ]

	def __str__(self):
		return self.name

Location.panels = [
	MultiFieldPanel([
			FieldRowPanel([
					FieldPanel('name', classname='col6'),
					FieldPanel('address', classname='col6')
				]
			),
		],
		heading='Locatie gegevens'
	)
]

@register_snippet
class Address(djangomodels.Model):

	city = djangomodels.CharField(verbose_name='stad', max_length=40)
	postal_code = djangomodels.CharField(verbose_name='postcode', max_length=8, null=True)
	street = djangomodels.CharField(verbose_name='straat', max_length=40, null=True)
	number = djangomodels.CharField(verbose_name='nummer', max_length=8, null=True)
	country = CountryField(verbose_name='land', null=True, default='BE')

	class Meta:
		verbose_name = 'adres'
		verbose_name_plural = 'adressen'
		ordering = ['city', ]

	def __str__(self):
		return '%s - %s' % (self.city, self.street)

Address.panels = [
	MultiFieldPanel([
			FieldRowPanel([
					FieldPanel('street', classname='col8'),
					FieldPanel('number', classname='col4')
				]
			),
			FieldRowPanel([
					FieldPanel('city', classname='col8'),
					FieldPanel('postal_code', classname='col4')
				]
			),
			FieldRowPanel([
					FieldPanel('country', classname='col6'),
				]
			),
		],
		heading='Adressgegevens'
	),
]

class HomePage(Page):
    template = 'home/home.html'

class ContactPage(Page):
	template = 'home/contact.html'

	#description = djangomodels.TextField(verbose_name='beschrijving', max_length=256)

class NewsArticle(Page):

	name = djangomodels.CharField(verbose_name='naam', max_length=164)
	# Streamfield goes here
	

NewsArticle.content_panels = [
	MultiFieldPanel([
			FieldRowPanel([
				FieldPanel('name',classname='col6'),
				]
			),
		],
		heading='Nieuws artikel')
]

class Blog(Orderable, Page):
	'''
	Dit model beschijft 1 enkele blog post. 
	TODO: 	mogelijk is het beter om de title block (en eventueel intro block) niet als streamfield onderdelen
			te definieren, maar als standaard attributen. Zo is het zeker dat elke blog post deze items bevat
	'''

	template = 'home/blog_page.html'

	date = djangomodels.DateField(verbose_name='blog datum', default=date.today)

	blog_content = fields.StreamField([
		('blog_title', BlogTitleBlock(help_text='Dit is de titel van het artikel, voorzien van een afbeelding')),
		('blog_intro', IntroTextBlock(help_text='Hiermee kan je optioneel een korte inleiding voorzien')),
		('blog_subtitle', SubtitleBlock()),	
		('blog_paragraph', ParagraphBlock()),
		('blog_image', ImageWithCaptionBlock()),
		('blog_quote', PullQuoteBlock()),
	], verbose_name='Blog inhoud')


#Blog.parent_page_types = ['home.BlogIndexPage', ]
Blog.subpage_types = []

Blog.content_panels = [
#	MultiFieldPanel([
#		FieldRowPanel([
#				FieldPanel('title', classname='col12'),
#				FieldPanel('author', classname='col6'),
#				FieldPanel('date_posted', classname='col6'),
#			]),
#		], heading='Blog informatie',
#	),
	StreamFieldPanel('blog_content'),
]

class CalenderEvent(Page):

	name = djangomodels.CharField(verbose_name='naam', max_length=164)
	description = djangomodels.TextField(verbose_name='beschrijving')
	event_date = djangomodels.DateField(verbose_name='datum', default=date.today)
	event_duration = djangomodels.PositiveIntegerField('Duur (# dagen)', default=1, validators=[MaxValueValidator(21),])
	website = djangomodels.URLField()

#FestivalPage.parent_page_types = ['home.FestivalIndexPage', ]
CalenderEvent.subpage_types = []

# Festival page panels
CalenderEvent.content_panels = [

	MultiFieldPanel([
			FieldRowPanel([
					FieldPanel('name', classname='col6'),
					FieldPanel('website', classname='col6'),
				]
			),
			
			FieldRowPanel([
				FieldPanel('event_date', classname='col6'),
				FieldPanel('event_duration', classname='col6'),
				],
			),
			FieldPanel('description'),
			#SnippetChooserPanel('contact_person', 'home.Person'),
			#SnippetChooserPanel('location', 'home.Location'),
			#FieldPanel('contact_person'),

		],
		heading='Evenement gegevens'
	),
]


