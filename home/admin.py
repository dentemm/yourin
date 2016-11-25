from django.contrib import admin

from .models import Category, EventCategory

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
	pass

@admin.register(EventCategory)
class EventCategoryAdmin(admin.ModelAdmin):
	pass
