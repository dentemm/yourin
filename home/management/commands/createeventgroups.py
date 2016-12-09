from django.core.management.base import BaseCommand, CommandError

#from datetime import datetime, timedelta

from home.models import Event, EventGroup


# 	template = 'home/event/event_detail.html'

# 	name = djangomodels.CharField(verbose_name='naam', max_length=164, default='', null=True, blank=True)
# 	description = djangomodels.TextField(verbose_name='beschrijving', null=True)
# 	website = djangomodels.URLField(verbose_name='website ', null=True)
# 	class_name = djangomodels.CharField(max_length=28, default='cal_event')
# 	tags = ClusterTaggableManager(through=EventTag, blank=True)

# 	image = djangomodels.ForeignKey('home.CustomImage', verbose_name='logo', null=True, blank=True, on_delete=djangomodels.SET_NULL, related_name='+')
# 	category = djangomodels.PositiveIntegerField(choices=EVENT_CATEGORY_CHOICES, default=1)

# class Command(BaseCommand):

# 	help = 'Create EventGroup for present Event objects'

# 	def handle(self, *args, **options):

# 		for event in Event.objects.all():

# 			new = EventGroup(title=event.title, template=event.template, name=event.name, description=event.description, website=event.website, 
# 					class_name=event.class_name, tags=event.tags, image=event.image, category=event.category)

# 			new.save()

# 		self.stdout.write(self.style.SUCCESS('Het is gefixt!'))