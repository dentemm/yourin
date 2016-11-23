from django.conf.urls import *

from . import views

urlpatterns = [
	
	url(r'^calendar/blogs_events/$', views.CalendarEventsApiView.as_view(), name='calendar-events'),
	
]