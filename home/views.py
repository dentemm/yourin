from datetime import timedelta, datetime, time

from django.urls import reverse
from django.views.generic import DetailView

from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response

from .models import Event, Blog, EventInstance
from .serializers import EventSerializer, BlogSerializer


class EventDetailView(DetailView):

	model = EventInstance
	template_name = 'home/event/event_detail.html'



#
#
# API VIEWS
#
#

class CalendarEventsApiView(APIView):

	def get(self, request, format=None):

		blogs = Blog.objects.live()
		event = Event.objects.live()

		blog_serializer = BlogSerializer(blogs, many=True)
		event_serializer = EventSerializer(events, many=True)

		#cal_events = list(blogs) + list(events)

		return Response(blog_serializer.data + event_serializer.data)


