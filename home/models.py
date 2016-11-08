from __future__ import absolute_import, unicode_literals

import geopy	# to geocode location data
from datetime import date

from django.db import models as djangomodels
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models.signals import pre_delete, pre_save
from django.utils.translation import ugettext_lazy as _
from django.dispatch import receiver

from wagtail.wagtailcore.models import Page, Orderable
from wagtail.wagtailcore import fields
from wagtail.wagtailadmin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel, FieldRowPanel, StreamFieldPanel
from wagtail.wagtailsnippets.models import register_snippet
from wagtail.wagtailimages.models import Image, AbstractImage, AbstractRendition
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailsearch import index

from django_countries.fields import CountryField

from .blocks import BlogTitleBlock, SubtitleBlock, IntroTextBlock, ParagraphBlock, ImageWithCaptionBlock, PullQuoteBlock
from .validators import validate_image_min, validate_blog_image

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
		verbose_name=_('file'), upload_to=get_upload_to, width_field='width', height_field='height', validators=[validate_image_min]
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

# @register_snippet
# class Influencer(djangomodels.Model):

@register_snippet
class EventCategory(djangomodels.Model):

	name = djangomodels.CharField(max_length=64)

	class Meta:
		verbose_name = 'Evenement Categorie'
		verbose_name_plural = 'Evenement Categorieën'
		ordering = ['name', ]

@register_snippet
class NewsCategory(djangomodels.Model):

	name = djangomodels.CharField(max_length=64)

	class Meta:
		verbose_name = 'Nieuwscategorie'
		verbose_name_plural = 'Nieuwscategorieën'
		ordering = ['name', ]

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
		heading='Adresgegevens'
	),
]

#
#
# CMS PAGES
#
#

class HomePage(Page):
    template = 'home/home.html'

HomePage.subpage_types = [
	'home.ContactPage',
	'home.AboutPage',
	'home.CalendarIndex',
	'home.BlogIndex',
	'home.InfluencerIndex',
]

class AboutPage(Page):
	template = 'home/about.html'

AboutPage.parent_page_types = [
	'home.HomePage',
]

AboutPage.subpage_types = []

class ContactPage(Page):
	template = 'home/contact.html'

ContactPage.parent_page_types = [
	'home.HomePage'
]

ContactPage.subpage_types = []

class CalendarPage(Page):
	template = 'home/calendar/calendar.html'

class NewsArticle(Page):

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

class Blog(Orderable, Page):
	'''
	Dit model beschijft 1 enkele blog post. 
	TODO: 	mogelijk is het beter om de title block (en eventueel intro block) niet als streamfield onderdelen
			te definieren, maar als standaard attributen. Zo is het zeker dat elke blog post deze items bevat
	'''
	template = 'home/blog/blog_detail.html'

	date = djangomodels.DateField(verbose_name='blog datum', default=date.today)
	intro_text = djangomodels.TextField(verbose_name='intro text', default='', blank=True, null=True)
	image = djangomodels.ForeignKey('home.CustomImage', verbose_name='afbeelding', null=True, 
		blank=True, on_delete=djangomodels.SET_NULL, related_name='+', validators=validate_blog_image
		)

	blog_content = fields.StreamField([
		('blog_title', BlogTitleBlock(help_text='Dit is de titel van het artikel, voorzien van een afbeelding')),
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

class BlogIndex(Page):

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

class EventIndex(Page):

	template = 'home/event/event_index.html'

EventIndex.parent_page_types = [
	'home.HomePage'
]

EventIndex.parent_page_types = [
	'home.Event'
]

class Event(Page):

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

class CalendarEvent(Page):

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

class CalendarIndex(Page):

	template = 'home/calendar/calendar.html'

CalendarIndex.parent_page_types = [
	'home.HomePage', 
]

CalendarIndex.subpage_types = [
	'home.CalendarEvent',
]

class InfluencerIndex(Page):
	template = 'home/influencer/influencer_page.html'

InfluencerIndex.parent_page_types = [
	'home.HomePage'
]

InfluencerIndex.subpage_types = [
	'home.Influencer',
]

class Influencer(Page):

	template = 'home/influencer/influencer_detail.html'

Influencer.content_panels = Page.content_panels + [

]

Influencer.parent_page_types = [
	'home.InfluencerIndex',
]

Influencer.subpage_types = []