from django.contrib import admin

from .models import Category, EventGroupCategory

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
	pass

@admin.register(EventGroupCategory)
class EventGroupCategoryAdmin(admin.ModelAdmin):
	pass
