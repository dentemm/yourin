from django.contrib import admin

from .models import Category, EventCategory, Event, Location, EventInstance, EventEventInstance

@admin.register(EventEventInstance)
class EventEventInstanceAdmin(admin.ModelAdmin):
	pass

@admin.register(EventInstance)
class EventInstanceAdmin(admin.ModelAdmin):
	pass

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
	pass

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
	pass

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
	pass

@admin.register(EventCategory)
class EventCategoryAdmin(admin.ModelAdmin):
	pass
