from django.contrib import admin
from .models import SearchQuery

@admin.register(SearchQuery)
class SearchQueryAdmin(admin.ModelAdmin):
    list_display = ('id', 'thumbnail_preview', 'method', 'created_at')
    list_filter = ('method', 'created_at')
    readonly_fields = ('created_at',) 
    
    ordering = ('-created_at',)