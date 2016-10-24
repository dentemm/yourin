from __future__ import absolute_import, unicode_literals

import geopy	# to geocode location data
from datetime import date

from django.db import models as djangomodels
from django.core.validators import MinValueValidator, MaxValueValidator

from wagtail.wagtailcore.models import Page
from wagtail.wagtailadmin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel, FieldRowPanel
from wagtail.wagtailsnippets.models import register_snippet


from django_countries.fields import CountryField


@register_snippet
class Location(djangomodels.Model):

	name = djangomodels.CharField(max_length=64)
	address = djangomodels.ForeignKey('home.Address', verbose_name='adres', related_name='location', null=True)
	longitude = djangomodels.DecimalField(max_digits=10, decimal_places=7, blank=True, null=True)
	latitude = djangomodels.DecimalField(max_digits=10, decimal_places=7, blank=True, null=True)


@register_snippet
class Address(djangomodels.Model):

	city = djangomodels.CharField(verbose_name='stad', max_length=40)
	postal_code = djangomodels.CharField(verbose_name='postcode', max_length=8, null=True)
	street = djangomodels.CharField(verbose_name='straat', max_length=40, null=True)
	number = djangomodels.CharField(verbose_name='nummer', max_length=8, null=True)
	country = CountryField(verbose_name='land', null=True, default='BE')

class HomePage(Page):
    pass

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
	#InlinePanel('rateable_attributes', label='Te beroordelen eigenschappen'),
	#InlinePanel('images', label='Festival afbeeldingen'),
	#InlinePanel('related_links', 
	#						label="URL's voor het festival",
	#						help_text=mark_safe('Bijkomende links voor een festival. Hier kan je ticket links, social media links en andere ingeven. Gebruik best een <b><u>consistente naam</u></b> voor gelijkaardige links, dus niet Facebook voor het ene, en FB voor het andere festival.')
	#						),
	#InlinePanel('locations', label='festival locaties (hoeft niet ingevuld te worden als er maar 1 locatie is)')
	#InlinePanel('persons', label='Maak nieuwe contactpersoon aan', max_num=1),
	#InlinePanel('rateable_attributes', label='Te beoordelen eigenschappen'),
	#CustomInlinePanel('rateable_attributes', label='Te beoordelen eigenschappen'),
]


