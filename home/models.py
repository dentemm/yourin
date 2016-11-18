from __future__ import absolute_import, unicode_literals

import geopy	# to geocode location data
from datetime import date

from django.db import models as djangomodels
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models.signals import pre_delete, pre_save
from django.utils.translation import ugettext_lazy as _
from django.utils.text import slugify
from django.dispatch import receiver


from wagtail.wagtailcore.models import Page, Orderable
from wagtail.wagtailcore import fields
from wagtail.wagtailadmin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel, FieldRowPanel, StreamFieldPanel
from wagtail.wagtailsnippets.models import register_snippet
from wagtail.wagtailimages.models import Image, AbstractImage, AbstractRendition
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailsearch import index

from modelcluster.fields import ParentalKey

from django_countries.fields import CountryField

from .blocks import BlogTitleBlock, SubtitleBlock, IntroTextBlock, ParagraphBlock, ImageWithCaptionBlock, PullQuoteBlock
from .validators import validate_image_min, validate_blog_image

#
#
# GLOBAL VARIABLES
#
#

yourin_variables = {}


RELATED_LINK_CHOICES = (
    (1, _("Facebook")),
    (2, _("Twitter")),
    (3, _("Youtube")),
)

#
#
# HELPER FUNCTIES
#
#
def get_upload_to(instance, filename):
    """
    Obtain a valid upload path for an image file.
    This needs to be a module-level function so that it can be referenced within migrations,
    but simply delegates to the `get_upload_to` method of the instance, so that AbstractImage
    subclasses can override it.
    """
    return instance.get_upload_to(filename)

#
#
# HELPER MODELLEN
#
#
class CustomImage(AbstractImage):
	'''
	Custom image model, om een auteur veld toe te voegen aan de wagtail Images
	'''

	file = djangomodels.ImageField(
		verbose_name=_('file'), upload_to=get_upload_to, width_field='width', height_field='height', validators=[validate_image_min, ]
	)

CustomImage.admin_form_fields = Image.admin_form_fields


class CustomRendition(AbstractRendition):
	'''
	Custom rendition model nodig wanneer je een custom image model toevoegt
	'''

	image = djangomodels.ForeignKey(CustomImage, related_name='renditions', db_constraint=False)

	class Meta:
		unique_together = (
			('image', 'filter', 'focal_point_key'),
		)

# Delete the source image file when an image is deleted
@receiver(pre_delete, sender=CustomImage)
def image_delete(sender, instance, **kwargs):
    instance.file.delete(False)

# Delete the rendition image file when a rendition is deleted
@receiver(pre_delete, sender=CustomRendition)
def rendition_delete(sender, instance, **kwargs):
    instance.file.delete(False)


#
#
# SNIPPETS 
#
#

@register_snippet
class EventCategory(djangomodels.Model):

	name = djangomodels.CharField(max_length=64)

	class Meta:
		verbose_name = 'Evenement Categorie'
		verbose_name_plural = 'Evenement Categorieën'
		ordering = ['name', ]

EventCategory.panels = [
	MultiFieldPanel([
			FieldRowPanel([
					FieldPanel('name', classname='col6'),
				]
			),
		]
	),
]

@register_snippet
class NewsCategory(djangomodels.Model):

	name = djangomodels.CharField(max_length=64)

	class Meta:
		verbose_name = 'Nieuwscategorie'
		verbose_name_plural = 'Nieuwscategorieën'
		ordering = ['name', ]

@register_snippet
class WhatWeDo(djangomodels.Model):

	name = djangomodels.CharField(verbose_name='naam', max_length=40)
	image = djangomodels.ForeignKey('home.CustomImage', verbose_name='afbeelding', null=True, blank=True, on_delete=djangomodels.SET_NULL, related_name='+')
	extra_info = djangomodels.TextField(verbose_name='info tekst', max_length=512)

	class Meta:
		verbose_name = 'pijler'
		verbose_name_plural = 'pijlers'


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
class Partner(djangomodels.Model):

	name = djangomodels.CharField(verbose_name='naam', max_length=64)
	website = djangomodels.URLField(verbose_name='website')
	description = djangomodels.TextField(verbose_name='beschrijving')
	logo = djangomodels.ForeignKey('home.CustomImage', null=True, blank=True, on_delete=djangomodels.SET_NULL, related_name='+')

	def __str__(self):
		return self.name

	class Meta:
		verbose_name = 'partner'
		verbose_name_plural = 'partners'
		ordering = ['name', ]

Partner.panels = [
	MultiFieldPanel([
			FieldRowPanel([
					FieldPanel('name', classname='col6'),
					FieldPanel('website', classname='col6')

				]
			),
			FieldRowPanel([
					FieldPanel('description'),
				]
			),
			ImageChooserPanel('logo'),

		], heading='Partner informatie'
	),
	#ImageChooserPanel('logo'),
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
		], heading='Adresgegevens'
	),
]

#
#
# CMS PAGES
#
#
class LinkFields(djangomodels.Model):

	link_external = djangomodels.URLField('Externe link', blank=True)
	link_page = djangomodels.ForeignKey(
		'wagtailcore.Page',
		null=True,
		blank=True,
		related_name='+'
	)

	class Meta:
		abstract = True

	@property
	def link(self):

		if self.link_page:
			return self.link_page.url

		else:
			return self.link_external

LinkFields.panels = [
	FieldPanel('link_external'),
]

class RelatedLink(LinkFields):

	#title = djangomodels.CharField('titel', max_length=63, help_text='Naam van link')

	title = djangomodels.IntegerField(verbose_name='Link naar', choices=RELATED_LINK_CHOICES)
	icon_class = ''

	class Meta:
		abstract = True

	def save(self, *args, **kwargs): # FB / TW / YOU

		if self.title == 1:
			self.icon_class = 'fa fa-facebook'

		elif self.title == 2:
			self.icon_class = 'fa fa-twitter'

		elif self.title == 3:
			self.icon_class = 'fa fa-youtube-play'

		else:
			self.icon_class = 'fa fa-external-link'

RelatedLink.panels = [
	FieldPanel('title'),
	MultiFieldPanel(LinkFields.panels, 'Link')
]

class HomePageNumbers(djangomodels.Model):

	name = djangomodels.CharField(verbose_name='naam', max_length=28)
	value = djangomodels.PositiveIntegerField(verbose_name='aantal', default=1)

class BasePage(Page):

	catchphrase = djangomodels.CharField(verbose_name='catchphrase', max_length=164, default='Entertainment voor jongeren')

	def get_context(self, request, *args, **kwargs):

		ctx = super(BasePage, self).get_context(request, *args, **kwargs)

		ctx['yourin'] = yourin_variables

		return ctx

	def save(self, *args, **kwargs):

		yourin_variables['catchphrase'] = self.catchphrase

		super(BasePage, self).save(*args, **kwargs)

	class Meta:
		abstract = True


class HomePage(BasePage):
    template = 'home/home.html'

    class Meta:
    	verbose_name = 'startpagina'


HomePage.content_panels = Page.content_panels + [
	MultiFieldPanel([
			FieldRowPanel([
					FieldPanel('catchphrase', classname='col12'),
				]
			),
		], heading='Startpagina aanpassingen'
	),
	InlinePanel('partners', label='Partners'),
]

HomePage.subpage_types = [
	'home.ContactPage',
	'home.AboutPage',
	'home.CalendarIndex',
	'home.BlogIndex',
	'home.InfluencerIndex',
	'home.EventIndex',
]

class YourinPartner(djangomodels.Model):
	'''
	Through / join model voor m2m relatie tussen Homepage en Partner
	'''

	partner = djangomodels.ForeignKey('home.Partner')
	page = ParentalKey('home.HomePage', related_name='partners')

	
YourinPartner.panels = [
	FieldPanel('partner'),
]

class AboutPage(BasePage):
	template = 'home/about.html'

AboutPage.parent_page_types = [
	'home.HomePage',
]

AboutPage.subpage_types = []

class ContactPage(BasePage):
	template = 'home/contact.html'

ContactPage.parent_page_types = [
	'home.HomePage',
]

ContactPage.subpage_types = []

class CalendarPage(BasePage):
	template = 'home/calendar/calendar_v2.html'

class NewsArticle(BasePage):

	template = 'home/article_page.html'

	pub_date = djangomodels.DateField(auto_now_add=True, null=True)
	update_date = djangomodels.DateField(auto_now=True, null=True)

	name = djangomodels.CharField(verbose_name='naam', max_length=164)
	image = djangomodels.ForeignKey('home.CustomImage', null=True, blank=True, on_delete=djangomodels.SET_NULL, related_name='+')
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

class Blog(Orderable, BasePage):
	'''
	Dit model beschijft 1 enkele blog post. 
	TODO: 	mogelijk is het beter om de title block (en eventueel intro block) niet als streamfield onderdelen
			te definieren, maar als standaard attributen. Zo is het zeker dat elke blog post deze items bevat
	'''
	template = 'home/blog/blog_detail.html'

	date = djangomodels.DateField(auto_now_add=True)
	edited = djangomodels.DateField(auto_now=True)
	intro_text = djangomodels.TextField(verbose_name='intro text', default='', blank=True, null=True)
	image = djangomodels.ForeignKey('home.CustomImage', verbose_name='afbeelding', null=True, 
		blank=True, on_delete=djangomodels.SET_NULL, related_name='+'
		)

	blog_content = fields.StreamField([
		#('blog_title', BlogTitleBlock(help_text='Dit is de titel van het artikel, voorzien van een afbeelding')),
		('blog_intro', IntroTextBlock(help_text='Hiermee kan je optioneel een korte inleiding voorzien')),
		('blog_subtitle', SubtitleBlock()),	
		('blog_paragraph', ParagraphBlock()),
		('blog_image', ImageWithCaptionBlock()),
		('blog_quote', PullQuoteBlock()),
	], verbose_name='Blog Inhoud')


Blog.parent_page_types = ['home.BlogIndex', ]
Blog.subpage_types = []

Blog.content_panels = [
	MultiFieldPanel([
		FieldRowPanel([
				FieldPanel('title', classname='col12'),
				FieldPanel('intro_text', classname='col6'),
				#FieldPanel('date_posted', classname='col6'),
			]),
		], heading='Blog informatie',
	),
	ImageChooserPanel('image'),
	StreamFieldPanel('blog_content'),
]

class BlogIndex(BasePage):

	template = 'home/blog/blog_page.html'

	intro = fields.RichTextField(blank=True)

	@property
	def blogs(self):
		# Get list of live blog pages that are descendants of this page
		blogs = Blog.objects.live().descendant_of(self)

		# Order by most recent date first
		blogs = blogs.order_by('-date')

		return blogs

	def get_context(self, request):
		# Get blogs
		blogs = self.blogs

		# Filter by tag (als die bestaat)
		tag = request.GET.get('tag')

		if tag:
			blogs = blogs.filter(tags__name=tag)

		# Pagination
		page = request.GET.get('page')
		paginator = Paginator(blogs, 3)  # Show 3 blogs per page

		try:
			blogs = paginator.page(page)

		except PageNotAnInteger:
			blogs = paginator.page(1)

		except EmptyPage:
			blogs = paginator.page(paginator.num_pages)

		# Update template context
		context = super(BlogIndex, self).get_context(request)
		context['blogs'] = blogs
		return context

BlogIndex.parent_page_types = [
	'home.HomePage',
]

BlogIndex.subpage_types = [
	'home.Blog',
]

BlogIndex.search_fields = Page.search_fields + [
	index.SearchField('intro'),
]

class EventIndex(BasePage):

	template = 'home/event/event_index.html'

	name = djangomodels.CharField(verbose_name='naam', max_length=164, default='')


EventIndex.content_panels = Page.content_panels + [
	MultiFieldPanel([
			FieldRowPanel([
				FieldPanel('name', classname='col6'),
				]
			),
		]
	),
]

EventIndex.parent_page_types = [
	'home.HomePage',
]

EventIndex.subpage_types = [
	'home.Event',
]

class Event(BasePage):

	template = 'home/event/event_detail.html'

	name = djangomodels.CharField(verbose_name='naam', max_length=164, default='')
	description = djangomodels.TextField(verbose_name='beschrijving', null=True)
	event_date = djangomodels.DateField(verbose_name='datum', default=date.today)
	event_duration = djangomodels.PositiveIntegerField('Duur (# dagen)', default=1, validators=[MaxValueValidator(21),])
	website = djangomodels.URLField(verbose_name='event website', null=True)

	image = djangomodels.ForeignKey('home.CustomImage', null=True, blank=True, on_delete=djangomodels.SET_NULL, related_name='+')
	category = djangomodels.ForeignKey('home.EventCategory', null=True, blank=True, on_delete=djangomodels.SET_NULL, related_name='events')

# Festival page panels
Event.content_panels = [

	MultiFieldPanel([
			FieldRowPanel([
				FieldPanel('name', classname='col6'),
				FieldPanel('category', classname='col6'),
				]
			),
			FieldRowPanel([
				FieldPanel('event_date', classname='col6'),
				FieldPanel('event_duration', classname='col6'),
				],
			),
			FieldRowPanel([
				FieldPanel('website', classname='col6'),
				],
			),
			FieldPanel('description'),
			ImageChooserPanel('image'),
		],
		heading='Evenement gegevens'
	),
]

Event.parent_page_types = [
	'home.EventIndex', 
]

Event.subpage_types = []

class CalendarEvent(BasePage):

	template = 'home/calendar/calendar_event.html'

	name = djangomodels.CharField(verbose_name='naam', max_length=164)
	description = djangomodels.TextField(verbose_name='beschrijving')
	event_date = djangomodels.DateField(verbose_name='datum', default=date.today)
	event_duration = djangomodels.PositiveIntegerField('Duur (# dagen)', default=1, validators=[MaxValueValidator(21),])
	website = djangomodels.URLField(verbose_name='event website')

	image = djangomodels.ForeignKey('home.CustomImage', null=True, blank=True, on_delete=djangomodels.SET_NULL, related_name='+')
	category = djangomodels.ForeignKey('home.EventCategory', null=True, blank=True, on_delete=djangomodels.SET_NULL, related_name='calendar_events')


CalendarEvent.parent_page_types = [
	'home.CalendarIndex', 
]

CalendarEvent.subpage_types = []

# Festival page panels
CalendarEvent.content_panels = [

	MultiFieldPanel([
			FieldRowPanel([
					FieldPanel('name', classname='col6'),
					FieldPanel('category', classname='col6'),
				]
			),
			FieldRowPanel([
				FieldPanel('event_date', classname='col6'),
				FieldPanel('event_duration', classname='col6'),
				],
			),
			FieldRowPanel([
				FieldPanel('website', classname='col6'),
				],
			),
			FieldPanel('description'),
			ImageChooserPanel('image'),
			#SnippetChooserPanel('contact_person', 'home.Person'),
			#SnippetChooserPanel('location', 'home.Location'),
			#FieldPanel('contact_person'),
		],
		heading='Evenement gegevens'
	),
]

class CalendarIndex(BasePage):

	template = 'home/calendar/calendar_v2.html'

CalendarIndex.parent_page_types = [
	'home.HomePage', 
]

CalendarIndex.subpage_types = [
	'home.CalendarEvent',
]

class InfluencerIndex(BasePage):
	template = 'home/influencer/influencer_page.html'

InfluencerIndex.parent_page_types = [
	'home.HomePage',
]

InfluencerIndex.subpage_types = [
	'home.Influencer',
]

class InfluencerRelatedLink(Orderable, RelatedLink):
	'''
	Deze klasse wordt gebruikt om externe links aan een influencer toe te kennen.
	Dit zijn links naar facebook, youtube en dergelijke
	'''

	page = ParentalKey('home.Influencer', related_name='related_links')


class Influencer(BasePage):

	template = 'home/influencer/influencer_detail.html'
	name = djangomodels.CharField(max_length=128)
	extra_info = djangomodels.TextField(verbose_name='Beschrijving', null=True)
	image = djangomodels.ForeignKey('home.CustomImage', verbose_name='afbeelding', null=True, blank=True, on_delete=djangomodels.SET_NULL, related_name='+')


Influencer.content_panels =  [
	MultiFieldPanel([
			FieldRowPanel([
				FieldPanel('title', classname='col6')
				]
			),
			FieldPanel('extra_info'),
			ImageChooserPanel('image'),
		], heading='Influencer'
	), 
	InlinePanel('related_links', 
		label='Externe links',
		help_text='Hier kan je links naar Youtube, FB en andere ingeven',
	),
]

Influencer.parent_page_types = [
	'home.InfluencerIndex',
]

Influencer.subpage_types = []