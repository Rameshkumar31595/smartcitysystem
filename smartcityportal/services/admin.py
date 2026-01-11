from django.contrib import admin
from .models import ServiceCategory, CityService

@admin.register(ServiceCategory)
class ServiceCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name', 'description')
    ordering = ('name',)

@admin.register(CityService)
class CityServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'contact_info')
    list_filter = ('category',)
    search_fields = ('name', 'description', 'contact_info')
    ordering = ('name',)
