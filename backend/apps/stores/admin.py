from django.contrib import admin
from .models import Store

@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ['name', 'optician_name', 'city', 'phone', 'is_active']
    search_fields = ['name', 'optician_name']
    prepopulated_fields = {'slug': ('name',)}