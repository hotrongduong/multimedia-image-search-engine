from django.contrib import admin
from .models import UploadedImage, SearchQuery

@admin.register(UploadedImage)
class UploadedImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'image_preview', 'user', 'uploaded_at')
    list_filter = ('user', 'uploaded_at')
    readonly_fields = ('uploaded_at',)

@admin.register(SearchQuery)
class SearchQueryAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_thumbnail', 'method', 'created_at')
    list_filter = ('method', 'created_at')
    
    def has_change_permission(self, request, obj=None):
        return False