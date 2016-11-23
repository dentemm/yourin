from rest_framework import serializers

from .models import Event, Blog

class EventSerializer(serializers.ModelSerializer):

	class Meta:
		model = Event
		fields = ('title', 'id', 'event_date')

class BlogSerializer(serializers.ModelSerializer):

	class Meta:
		model = Blog
		fields = ('title', 'id', 'date')

