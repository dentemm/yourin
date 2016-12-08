from django.contrib import admin

from .models import Category, EventCategory, Event

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
	pass

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
	pass

@admin.register(EventCategory)
class EventCategoryAdmin(admin.ModelAdmin):
	pass
