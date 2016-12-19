from __future__ import absolute_import, unicode_literals

import os
import geopy	# to geocode location data
from datetime import date, timedelta

from django.db import models as djangomodels
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.exceptions import ValidationError
from django.template.response import TemplateResponse
from django.db.models.signals import pre_delete, pre_save
from django.utils.translation import ugettext_lazy as _
from django.utils.text import slugify
from django.dispatch import receiver

from wagtail.wagtailcore.models import Page, Orderable
from wagtail.wagtailcore import fields
from wagtail.wagtailcore.blocks import ListBlock
from wagtail.wagtailadmin.forms import WagtailAdminPageForm, WagtailAdminModelForm
from wagtail.wagtailadmin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel, FieldRowPanel, StreamFieldPanel, PageChooserPanel
from wagtail.wagtailsnippets.models import register_snippet
from wagtail.wagtailimages.models import Image, AbstractImage, AbstractRendition
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailsearch import index
from wagtail.wagtailembeds.blocks import EmbedBlock
from wagtail.contrib.wagtailroutablepage.models import RoutablePageMixin, route

from wagtail.wagtailadmin.forms import WagtailAdminPageForm, WagtailAdminModelForm

from modelcluster.fields import ParentalKey
from modelcluster.tags import ClusterTaggableManager

from taggit.models import TaggedItemBase

from django_countries.fields import CountryField

from . import blocks as customblocks
from .blocks import BlogTitleBlock, SubtitleBlock, IntroTextBlock, ParagraphBlock, ImageWithCaptionBlock, PullQuoteBlock, BlogEmbedBlock
from .validators import validate_image_min, validate_blog_image
from .variables import RELATED_LINK_CHOICES, ICON_CHOICES, ICON_COLOR_CHOICES, EVENT_CATEGORY_CHOICES

#
#
# GLOBAL VARIABLES
#
#
yourin_variables = {}


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
	Custom image model, om bijkomende field validation toe te voegen
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
			('image', 'filter_spec', 'focal_point_key'),
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

#@register_snippet
class Category(djangomodels.Model):

	name = djangomodels.PositiveIntegerField(verbose_name='categorie', choices=EVENT_CATEGORY_CHOICES, default=1)
	#image = djangomodels.ForeignKey('home.CustomImage', verbose_name='afbeelding', null=True, blank=True, on_delete=djangomodels.SET_NULL, related_name='+')


	class Meta:
		verbose_name = 'Evenement Categorie'
		verbose_name_plural = 'Evenement Categorieën'
		ordering = ['name', ]

	def __str__(self):
		return self.name

Category.panels = [
	MultiFieldPanel([
			FieldRowPanel([
					FieldPanel('name', classname='col6', ),
				]
			),
			ImageChooserPanel('image'),
		], heading='Categorie',
	), 

]

@register_snippet
class Address(djangomodels.Model):

	city = djangomodels.CharField(verbose_name='stad', max_length=40)
	postal_code = djangomodels.CharField(verbose_name='postcode', max_length=8)
	street = djangomodels.CharField(verbose_name='straat', max_length=40)
	number = djangomodels.CharField(verbose_name='nummer', max_length=8)
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

@register_snippet
class Location(Address):

	name = djangomodels.CharField(verbose_name='naam locatie', max_length=64)
	longitude = djangomodels.DecimalField(max_digits=10, decimal_places=7, blank=True, null=True)
	latitude = djangomodels.DecimalField(max_digits=10, decimal_places=7, blank=True, null=True)

	class Meta:
		verbose_name = 'locatie'
		verbose_name_plural = 'locaties'
		ordering = ['name', ]

	def __str__(self):
		return self.name

	def save(self, *args, **kwargs):

		geolocator = geopy.geocoders.Nominatim()
		address_string = self.street + ' ' + self.number + ' ' + self.postal_code + ' ' + self.city + ' ' + str(self.country.name)

		loc = geolocator.geocode(address_string)

		if not isinstance(loc, geopy.location.Location):

			alternative = self.street + ' ' + self.postal_code + ' ' + self.city + ' ' + str(self.country.name)
			loc = geolocator.geocode(alternative)

		if isinstance(loc, geopy.location.Location):

			self.latitude = loc.latitude
			self.longitude = loc.longitude

		return super(Location, self).save(*args, **kwargs)

Location.panels = [
	MultiFieldPanel([
			FieldRowPanel([
					FieldPanel('name', classname='col6'),
					#FieldPanel('address', classname='col6')
				]	
			),
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
		heading='Locatie gegevens'
	)
]

class EventInstanceImage(djangomodels.Model):

	image = djangomodels.ForeignKey('home.CustomImage')
	caption = djangomodels.CharField(max_length=63, null=True, blank=True)

class EventInstance(djangomodels.Model):

	title = djangomodels.CharField(verbose_name='naam', max_length=128)
	event_description = djangomodels.TextField(verbose_name='beschrijving', null=True)
	event_date = djangomodels.DateField(verbose_name='datum', default=date.today)
	location = djangomodels.ForeignKey('home.Location', verbose_name='locatie', null=True, on_delete=djangomodels.SET_NULL)
	website = djangomodels.URLField(null=True, blank=True)
	image = djangomodels.ForeignKey('home.CustomImage', null=True)

	class Meta:
		verbose_name = 'evenement'
		verbose_name_plural = 'evenementen'
		ordering = ['-event_date', 'title']

	def __str__(self):
		return self.title

	def category(self):
		'''
		Found a way to access the parent (relation from ParentalKey)
		'''

		event_event_instance = EventEventInstance.objects.get(title=self.title)
		page = event_event_instance.page

		return page.get_category_display()

EventInstance.panels = [
	MultiFieldPanel([
			FieldRowPanel([
				FieldPanel('title',  classname='col6'),
				FieldPanel('event_date', classname='col6')
				]
			),
			FieldRowPanel([
				FieldPanel('website', classname='col6'),
				FieldPanel('location', classname='col6')
				]
			),
			FieldRowPanel([
				FieldPanel('event_description', classname='col12'),
				]
			),
			ImageChooserPanel('image'),
		], heading='Evenement data'
	),
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
]

class WhatWeDo(djangomodels.Model):

	name = djangomodels.CharField(verbose_name='naam', max_length=40)
	text_color = djangomodels.CharField(verbose_name='tekstkleur', max_length=32, choices=ICON_COLOR_CHOICES, default='text-default')
	image = djangomodels.ForeignKey('home.CustomImage', verbose_name='afbeelding', null=True, blank=True, on_delete=djangomodels.SET_NULL, related_name='+')
	extra_info = djangomodels.TextField(verbose_name='info tekst', max_length=180, null=True, blank=True)
	icon = djangomodels.CharField(max_length=28, choices=ICON_CHOICES, default='fa fa-commenting-o')
	related_page = djangomodels.ForeignKey('wagtailcore.Page', verbose_name='Link naar pagina', null=True, blank=True, on_delete=djangomodels.SET_NULL, related_name='+')

	class Meta:
		verbose_name = 'homepage pijler'
		verbose_name_plural = 'homepage pijlers'

WhatWeDo.panels = [
	MultiFieldPanel([
			FieldRowPanel([
					FieldPanel('name', classname='col6'),
					FieldPanel('icon', classname='col6')
				],
			),
			FieldRowPanel([
					FieldPanel('text_color', classname='col6')
				],
			),			
			FieldRowPanel([
					FieldPanel('extra_info', classname='col9')
				],
			),
			ImageChooserPanel('image'),
			PageChooserPanel('related_page', ['home.InfluencerIndex', 'home.BlogIndex', 'home.EventIndex', 'home.ContactPage', 'home.AboutPage', 'home.CalendarIndex' ])

		], heading="Yourin 'pijlers'"
	)
]

class Numbers(djangomodels.Model):

	name = djangomodels.CharField(verbose_name='naam', max_length=28)
	value = djangomodels.PositiveIntegerField(verbose_name='cijfer', default=1)
	icon = djangomodels.CharField(verbose_name='icoon', max_length=28, choices=ICON_CHOICES, default='fa fa-bar-chart')
	icon_color = djangomodels.CharField(verbose_name='kleur icoon', max_length=32, choices=ICON_COLOR_CHOICES, default='text-default')

Numbers.panels = [
	MultiFieldPanel([
			FieldRowPanel([
				FieldPanel('name', classname='col6'),
				FieldPanel('value', classname='col6')
				]
			),
			FieldRowPanel([
				FieldPanel('icon', classname='col6'),
				FieldPanel('icon_color', classname='col6')
				]
			),
		], heading="Marketing cijfers"
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

	@property
	def icon(self):

		return self.icon_class

LinkFields.panels = [
	FieldPanel('link_external'),
]

class RelatedLink(LinkFields):

	#title = djangomodels.CharField('titel', max_length=63, help_text='Naam van link')

	title = djangomodels.IntegerField(verbose_name='Link naar', choices=RELATED_LINK_CHOICES)
	icon_class = djangomodels.CharField(max_length=128, null=True, blank=True)

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

		print('icon class: %s' % self.icon_class)

		return super(RelatedLink, self).save(*args, **kwargs)

RelatedLink.panels = [
	FieldPanel('title'),
	MultiFieldPanel(LinkFields.panels, 'Link')
]

class BasePage(Page):

	has_subtitle = djangomodels.BooleanField(verbose_name='Subtitel balk', default=True)

	@property
	def footer_blogs(self):
		# Get list of live blog pages that are descendants of this page
		blogs = Blog.objects.live().order_by('-date')[:3]

		return blogs

	class Meta:
		abstract = True

	def get_context(self, request, *args, **kwargs):

		ctx = super(BasePage, self).get_context(request, *args, **kwargs)

		ctx['yourin'] = yourin_variables
		ctx['footer_blogs'] = self.footer_blogs

		return ctx

class HomePageContent(Orderable, WhatWeDo):

	page = ParentalKey('home.HomePage', related_name='contents')

class HomePageNumbers(Orderable, Numbers):

	page = ParentalKey('home.HomePage', related_name='numbers')

class HomePage(BasePage):

	template = 'home/home.html'
	intro_image = djangomodels.ForeignKey('home.CustomImage', null=True, blank=True, on_delete=djangomodels.SET_NULL, related_name='home_intro_images')

	catchphrase = djangomodels.CharField(verbose_name='catchphrase', max_length=164, default='Entertainment voor jongeren')
	catchphrase_color = djangomodels.CharField(verbose_name='catchphrase kleur', max_length=32, choices=ICON_COLOR_CHOICES, default='text-default')
	fb_link = djangomodels.URLField(verbose_name='FB pagina', default='https://www.facebook.com/yourin.be/')
	twitter_link = djangomodels.URLField(verbose_name='Twitter pagina', default='https://twitter.com/yourinbe')
	linkedin_link = djangomodels.URLField(verbose_name='LinkedIn pagina', default='https://www.linkedin.com/company/4982091')
	youtube_link = djangomodels.URLField(verbose_name='Youtube kanaal', default='https://www.youtube.com/user/yourinbe')

	class Meta:
		verbose_name = 'startpagina'

	@property
	def recents(self):

		print('RECENTS')

		# 1. Latest blog article
		try:
			last_blog = Blog.objects.live().latest('date')

		except:
			last_blog = ''

		# 2. Latest event in past
		try:
			last_event = EventInstance.objects.filter(event_date__lt=date.today())[0]

		except:
			last_event = ''

		# 3. First two upcoming events
		try:
			upcoming = EventInstance.objects.filter(event_date__gte=date.today())[:2]

		except:
			upcoming = ['', '']

		if len(upcoming) < 2:
			upcoming = ['', '']

		#last_festival = Event.objects.live().filter(category=3)
		#last_camp = Event.objects.live().filter(category=2)
		#last_event = EventInstance.objects.all().latest('event_date')

		print('last event: %s' % last_event)

		return {
			'last_event': last_event,
			'next1': upcoming[0],
			'blog': last_blog,
			'next2': upcoming[1],
		}

	def serve(self, request):

		self.update_vars()
		
		return super(HomePage, self).serve(request)


	def save(self, *args, **kwargs):

		self.update_vars()

		super(HomePage, self).save(*args, **kwargs)

	def update_vars(self):

		yourin_variables['catchphrase'] = self.catchphrase
		yourin_variables['fb_link'] = self.fb_link
		yourin_variables['twitter_link'] = self.twitter_link
		yourin_variables['linkedin_link'] = self.linkedin_link
		yourin_variables['youtube_link'] = self.youtube_link

HomePage.content_panels = Page.content_panels + [
	MultiFieldPanel([
			FieldRowPanel([
					FieldPanel('catchphrase', classname='col12'),
					FieldPanel('catchphrase_color', classname='col12')
				]
			),
			ImageChooserPanel('intro_image'),
		], heading='Startpagina aanpassingen'
	),
	MultiFieldPanel([
			FieldRowPanel([
				FieldPanel('fb_link', classname='col6'),
				FieldPanel('twitter_link', classname='col6')
				],
			),
			FieldRowPanel([
				FieldPanel('youtube_link', classname='col6'),
				FieldPanel('linkedin_link', classname='col6')
				]
			),
		], heading='Yourin links'
	),
	InlinePanel('contents', label='Pijlers', help_text='Hiermee kan je de inhoud van de startpagina instellen. Dit zijn de zogenaamde pijlers van Yourin, en deze kunnen gewijzigd, verwijderd en toegevoegd worden.'),
	InlinePanel('numbers', label='Marketing numbers', help_text='Dit zijn enkele cijfers die op de startpagina worden weergegeven. Er zijn een aantal icoontjes gedefinieerd, maar deze lijst kan op vraag eenvoudig worden uitgebreid!'),
	InlinePanel('partners', label='Partners'),
]

HomePage.subpage_types = [
	'home.ContactPage',
	'home.AboutPage',
	'home.CalendarIndex',
	'home.BlogIndex',
	'home.InfluencerIndex',
	'home.EventIndex',
	'home.DynamicPage',
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

	date = djangomodels.DateField(auto_now_add=True, null=True)
	edited = djangomodels.DateField(auto_now=True, null=True)

	intro = fields.RichTextField(verbose_name='inhoud - alternatief', blank=True, null=True)

	page_content = fields.StreamField([
		('subtitle', SubtitleBlock()),
		('paragraph', ParagraphBlock()),
		('image', ImageWithCaptionBlock()),
		('quote', PullQuoteBlock()),
		('video', BlogEmbedBlock()),
		], verbose_name='Over ons pagina - inhoud', null=True)


	class Meta:
		verbose_name = 'over ons pagina'
		verbose_name_plural = "over ons pagina's"

	def __str__(self):
		return self.title


AboutPage.parent_page_types = [
	'home.HomePage',
]

AboutPage.subpage_types = []


AboutPage.content_panels = Page.content_panels + [
	MultiFieldPanel([
			FieldRowPanel([
				FieldPanel('has_subtitle', classname='col6')
				]
			),
			FieldRowPanel([
				FieldPanel('intro', classname='col6')
				]
			),
		], heading='Over ons - pagina data'
	),
	StreamFieldPanel('page_content'),
]



class ContactLocation(Orderable, Location):

	page = ParentalKey('home.ContactPage', related_name='locations')

class ContactPage(BasePage):

	template = 'home/contact.html'

	intro_text = djangomodels.CharField(max_length=255, default='''Vivamus sagittis lacus vel augue laoreet rutrum faucibus 
																dolor auctor. Cras justo odio, dapibus ac facilisis in, egestas 
																eget quam. Cras mattis consectetur purus sit amet fermentum.''')
	email = djangomodels.EmailField('contact email', default='ditishet_emailadresvoor@contactformulier.website')
	phone = djangomodels.CharField('telefoonnr', max_length=28, null=True, blank=True)

	@property
	def address(self):

		#print('ADDRESS: %s' % self.locations.all)

		address = ''

		for location in self.locations.all():

			current = location.street + ' ' + location.number + ', ' + location.city

			#print('ADDRESS: %s' % current)

			address = current

		return address

ContactPage.content_panels = Page.content_panels + [
	MultiFieldPanel([
			FieldRowPanel([
				FieldPanel('email', classname='col8'),
				]
			),
			FieldRowPanel([
				FieldPanel('phone', classname='col6'),
				#FieldPanel('address', classname='col6')
				]
			),
			FieldRowPanel([
				FieldPanel('intro_text', classname='col8')
				]
			),
		], heading='Details voor contactpagina',
	),
	InlinePanel('locations', label='locatie / adres van Yourin')

]

ContactPage.parent_page_types = [
	'home.HomePage',
]

ContactPage.subpage_types = []

class CalendarPage(BasePage):
	template = 'home/calendar/calendar_v2.html'

class BlogTag(TaggedItemBase):
    content_object = ParentalKey('home.Blog', related_name='tagged_items')

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
	class_name = djangomodels.CharField(max_length=28, default='cal_blog')
	tags = ClusterTaggableManager(through=BlogTag, blank=True)

	image = djangomodels.ForeignKey('home.CustomImage', verbose_name='afbeelding', null=True, 
		blank=True, on_delete=djangomodels.SET_NULL, related_name='blog_images'
		)

	blog_content = fields.StreamField([
		#('blog_title', BlogTitleBlock(help_text='Dit is de titel van het artikel, voorzien van een afbeelding')),
		#('blog_intro', IntroTextBlock(help_text='Hiermee kan je optioneel een korte inleiding voorzien')),
		#('blog_subtitle', SubtitleBlock()),	
		('blog_paragraph', ParagraphBlock()),
		('blog_image', ImageWithCaptionBlock()),
		('blog_quote', PullQuoteBlock()),
		('blog_video', BlogEmbedBlock()),
	], verbose_name='Blog Inhoud')


Blog.parent_page_types = ['home.BlogIndex', ]
Blog.subpage_types = []

Blog.content_panels = [
	MultiFieldPanel([
		FieldRowPanel([
				FieldPanel('title', classname='col6'),
				FieldPanel('intro_text', classname='col10'),
				#FieldPanel('date_posted', classname='col6'),
			]),
		ImageChooserPanel('image'),

		], heading='Blog informatie',
	),
	
	StreamFieldPanel('blog_content'),
	FieldPanel('tags')
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

	@property
	def recent_blogs(self):

		blogs = Blog.objects.live().descendant_of(self).order_by('-date')[:5]

		#blogs = blogs.order_by('-date')

		return blogs

	def get_context(self, request):
		# Get blogs
		blogs = self.blogs
		recent_blogs = self.recent_blogs

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
		context['recent_blogs'] = recent_blogs

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

class EventIndex(RoutablePageMixin, BasePage):

	template = 'home/event/event_index.html'

	# @route(r'^$', name='main')
	# @route(r'^page/(?P<page>\d+)/$', name='page')
	# def serve_page(self, request, page=0):

	# 	self.page = page 

	# 	print('SERVING PAGE')
		

	# 	return TemplateResponse(request, template=self.template, context=self.get_context(request))

	def get_context(self, request):

		print('homen we hier???')

		print('GET CONTEXT, page: %s' % self.page)

		ctx = super(EventIndex, self).get_context(request)

		return ctx


	@property
	def limited_events(self):

		today = date.today()
		start_date = today - timedelta(days=60)
		end_date = today + timedelta(days=60)

		events = Event.objects.live().descendant_of(self).filter(event_date__range=[start_date, end_date]).order_by('-event_date')

		return events

	def mini_cal_events(self):

		return self.date_filtered_qs(-60, 60)

	def date_filtered_qs(self, start, end):

		today = date.today()

		start = today + timedelta(days=start)
		end = today + timedelta(days=end)

		#return Event.objects.live().descendant_of(self).filter(event_date__range=[start, end]).order_by('-event_date')
		return Event.objects.live().descendant_of(self)

	@property
	def events(self):

		events = Event.objects.live().descendant_of(self)

		return events

	@property
	def upcoming_events(self):

		events = Event.objects.live().descendant_of(self)[:4]

		return events

	def get_context(self, request):
		# Get blogs
		events = self.events
		upcoming_events = self.upcoming_events

		# Update template context
		context = super(EventIndex, self).get_context(request)
		context['events'] = events
		context['upcoming_events'] = upcoming_events

		return context

EventIndex.content_panels = [
	MultiFieldPanel([
			FieldRowPanel([
				FieldPanel('title', classname='col6'),
				FieldPanel('has_subtitle', classname='col6')
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

class EventCategory(Category):

	page = ParentalKey('home.Event', related_name='categories')

class EventTag(TaggedItemBase):

    content_object = ParentalKey('home.Event', related_name='tagged_items')

class EventLocation(Orderable, Location):

	page = ParentalKey('home.Event', related_name='locations')


class EventEventInstance(Orderable, EventInstance):

	page = ParentalKey('home.Event', related_name='events')

class Event(BasePage):

	template = 'home/event/event_group.html'

	name = djangomodels.CharField(verbose_name='naam', max_length=164, default='', null=True, blank=True)
	subtitle = djangomodels.CharField(verbose_name='korte intro', max_length=120, null=True, blank=True)
	description = djangomodels.TextField(verbose_name='beschrijving', null=True)
	intro = fields.RichTextField(verbose_name='beschrijving(alternatief)', blank=True, null=True)
	website = djangomodels.URLField(verbose_name='website ', null=True)
	class_name = djangomodels.CharField(max_length=28, default='cal_event')
	tags = ClusterTaggableManager(through=EventTag, blank=True)

	image = djangomodels.ForeignKey('home.CustomImage', verbose_name='logo', null=True, blank=True, on_delete=djangomodels.SET_NULL, related_name='+')
	picture = djangomodels.ForeignKey('home.CustomImage', verbose_name='foto', null=True, blank=True, on_delete=djangomodels.SET_NULL, related_name='+')
	category = djangomodels.PositiveIntegerField(choices=EVENT_CATEGORY_CHOICES, default=1)

	class Meta:
		verbose_name = 'event groep'
		verbose_name_plural = 'event groepen'

	# @property
	# def related_events(self):

	# 	Event.objects.live().descendant_of(self).filter(event_date__range=[start_date, end_date]).order_by('-event_date')

	# 	return Event.objects.live().filter(category=self.category).exclude(name=self.name).order_by('-event_date')


	@property
	def icon(self):
		'''
		De verschillende categorieen worden elk voorzien van een icoon en kleur
		'''

		if self.category == 1:
			return 'fa fa-flash icon-danger'

		elif self.category == 2:
			return 'glyphicon glyphicon-tent icon-deluge'

		elif self.category == 3:
			return 'fa fa-map-signs icon-blue-gray-filled'

		elif self.category == 4:
			return 'fa fa-group icon-mantis-filled'

		else:
			return 'fa fa-gift icon-danger'



# Festival page panels
Event.content_panels = [

	MultiFieldPanel([
			FieldRowPanel([
				FieldPanel('title', classname='col6'),
				FieldPanel('category', classname='col6'),
				]
			),
			FieldRowPanel([
				FieldPanel('subtitle', classname='col6'),
				FieldPanel('website', classname='col6'),
				],
			),
			FieldPanel('description'),
			FieldPanel('intro'),
			ImageChooserPanel('image'),
			#FieldPanel('tags'),
		],
		heading='Evenement gegevens'
	),
	#InlinePanel('locations', label='locatie'),
	InlinePanel('events', label='evenementen')
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
	category = djangomodels.ForeignKey('home.Category', null=True, blank=True, on_delete=djangomodels.SET_NULL, related_name='calendar_events')


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

	@property
	def influencers(self):
		# Get list of live blog pages that are descendants of this page
		influencers = Influencer.objects.live().descendant_of(self)

		# Order by most recent date first
		influencers = influencers.order_by('-name')

		return influencers

	def get_context(self, request):
		# Get blogs
		influencers = self.influencers

		# Filter by tag (als die bestaat)
		tag = request.GET.get('tag')

		if tag:
			influencers = influencers.filter(tags__name=tag)

		# Pagination
		page = request.GET.get('page')
		paginator = Paginator(influencers, 3)  # Show 3 blogs per page

		try:
			influencers = paginator.page(page)

		except PageNotAnInteger:
			influencers = paginator.page(1)

		except EmptyPage:
			influencers = paginator.page(paginator.num_pages)

		# Update template context
		context = super(InfluencerIndex, self).get_context(request)
		context['influencers'] = influencers

		return context

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
	#base_form_class = InfluencerForm

	name = djangomodels.CharField(max_length=128, null=True, blank=False)
	extra_info = djangomodels.TextField(verbose_name='Beschrijving', null=True)
	quote = djangomodels.CharField(verbose_name='Influencer citaat', max_length=255, blank=True, null=True)
	image = djangomodels.ForeignKey('home.CustomImage', verbose_name='afbeelding', null=True, blank=True, on_delete=djangomodels.SET_NULL, related_name='+')

	def clean(self):
		'''
		See here for solution: https://github.com/wagtail/wagtail/issues/161
		'''

		super(Influencer, self).clean()

		if self.slug == '' or self.title == '':

			for influencer in Influencer.objects.all():

				if influencer.name == self.name:
					raise ValidationError({'slug': _("Er bestaat al een influencer met de naam die je hebt ingegeven!")})

			self.title = self.name
			self.slug = slugify(self.name)


# Line below is to fix slug related issues
Influencer._meta.get_field('slug').default='blank-slug'

Influencer.content_panels =  [
	MultiFieldPanel([
			FieldRowPanel([
				FieldPanel('name', classname='col6')
				]
			),
			FieldPanel('extra_info'),
			FieldPanel('quote'),
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



class DynamicPage(BasePage):
	template = 'home/dynamic.html'

	page_title = djangomodels.CharField(verbose_name='pagina titel', max_length=36, default='Dit is de grote ondertitel')
	page_icon = djangomodels.CharField(verbose_name='pagina icoon', max_length=28, choices=ICON_CHOICES, default='fa fa-commenting-o')


	page_content = fields.StreamField([
		#('carousel', CarouselBlock()),
		('subtitle', SubtitleBlock()),
		('paragraph', ParagraphBlock()),
		('image', ImageWithCaptionBlock()),
		('quote', PullQuoteBlock()),
		('tabs', ListBlock(customblocks.TabbedContentItem(), template='home/blocks/tabbed_content_block.html', icon='list-ul')),
		('video', BlogEmbedBlock()),
		('two_cols', customblocks.TwoColsBlock(classname='range')),
		('slider', ListBlock(customblocks.CarouselImageBlock(), template='home/blocks/carousel_block.html', icon='image'))
		], verbose_name='pagina inhoud', null=True)


	class Meta:
		verbose_name = 'dynamische pagina'
		verbose_name_plural = "dynamische pagina's"

	def __str__(self):
		return self.title


DynamicPage.parent_page_types = [
	'home.HomePage',
]

DynamicPage.subpage_types = []


DynamicPage.content_panels = Page.content_panels + [
	MultiFieldPanel([
			FieldRowPanel([
				FieldPanel('page_title', classname='col6'),
				FieldPanel('page_icon', classname='col6')
				]
			),
		], heading='pagina details'
	),
	StreamFieldPanel('page_content'),
]
