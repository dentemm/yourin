from datetime import timedelta, datetime, time

from django.urls import reverse

from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response

from .models import Event, Blog
from .serializers import EventSerializer, BlogSerializer


#
#
# API VIEWS
#
#

class CalendarEventsApiView(APIView):

	def get(self, request, format=None):

		blogs = Blog.objects.live()
		events = Event.objects.live()

		blog_serializer = BlogSerializer(blogs, many=True)
		event_serializer = EventSerializer(events, many=True)

		cal_events = list(blogs) + list(events)

		return Response(blog_serializer.data + event_serializer.data)


class TasksForEventApiView(APIView):
	'''
	Dit view retourneert een JSON response van alle taken voor een bepaald event. 
	Deze taken worden gebruikt door FullCalendar
	'''

	def dispatch(self, request, *args, **kwargs):

		self.event_id = kwargs.pop('event_id', None)

		return super(TasksForEventApiView, self).dispatch(request, *args, **kwargs)


	def get(self, request, format=None):

		# FullCalandar verwacht een events JSON list 

		tasks = Task.objects.filter(event__pk=self.event_id)

		events = []

		for task in tasks:

			color = get_color_for_task(task)

			events.append({
				'id': task.pk, 'resourceId': task.owner.pk, 'start': task.start_datetime, 'end': task.due_datetime, 'title': task.title, 'color': color
			})

		return Response(events)
		
class ResourcesForEventApiView(APIView):
	'''
	Dit view retourneert een JSON response van alle resources (= imec medewerkers) voor een bepaald event.
	Deze resources worden gebruikt door FullCalendar
	'''

	def dispatch(self, request, *args, **kwargs):

		self.event_id = kwargs.pop('event_id', None)

		return super(ResourcesForEventApiView, self).dispatch(request, *args, **kwargs)

	def get(self, request, format=None):

		tasks = Task.objects.filter(event__pk=self.event_id)

		resources = []

		for task in tasks:
			resources.append({
				'id': task.owner.user.id, 'title': task.owner.user.username
			})

		return Response(resources)

class ActivitiesForToolApiView(APIView):

	def dispatch(self, request, *args, **kwargs):

		self.tool_id = kwargs.pop('tool_id', None)

		print('tool id: %s' % self.tool_id)

		return super(ActivitiesForToolApiView, self).dispatch(request, *args, **kwargs)

	def get(self, request, format=None):

		tool = ToolPage.objects.get(pk=self.tool_id)
		tool_tasks = tool.loose_tasks

		tool_events = EventPage.objects.filter(module__tool__pk=self.tool_id)

		events = []

		for task in tool_tasks:

			color = get_color_for_task(task)

			events.append({
				'id': task.pk, 'resourceId': task.owner.pk, 'start': task.start_datetime, 'end': task.due_datetime, 'title': task.title, 'color': color
			})

		for event in tool_events:

			color = '#9f86ff'

			events.append({
				'id': event.slug, 'resourceId': event.responsible.pk, 'start': event.start_date, 'end': event.end_date, 'title': event.name, 'color': color
			})

		return Response(events)

class ResourcesForToolApiView(APIView):

	def dispatch(self, request, *args, **kwargs):

		self.tool_id = kwargs.pop('tool_id', None)

		print('tool id: %s' % self.tool_id)

		return super(ResourcesForToolApiView, self).dispatch(request, *args, **kwargs)

	def get(self, request, format=None):

		tool = ToolPage.objects.get(pk=self.tool_id)
		tool_tasks = tool.loose_tasks

		tool_events = EventPage.objects.filter(module__tool__pk=self.tool_id)

		resources = []

		for task in tool_tasks:
			resources.append({
				'id': task.owner.user.id, 'title': task.owner.user.username
			})

		for event in tool_events:

			resources.append({
				'id': event.responsible.pk, 'title': event.responsible.username
			})

		return Response(resources)
