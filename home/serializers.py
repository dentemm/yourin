from rest_framework import serializers

from .models import EventGroup, Blog

class EventSerializer(serializers.ModelSerializer):

	class Meta:
		model = EventGroup
		fields = ('title', 'id', 'event_date', 'url')

class BlogSerializer(serializers.ModelSerializer):

	class Meta:
		model = Blog
		fields = ('title', 'id', 'date', 'url')

