from django.contrib import admin

from .models import Category, EventCategory, Event, Location, EventInstance

@admin.register
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
