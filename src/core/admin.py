from django.contrib import admin
from .models import ImageMetadata

@admin.register(ImageMetadata)
class ImageMetadataAdmin(admin.ModelAdmin):
    list_display = ('id', 'thumbnail_preview', 'filename', 'get_tags_display', 'uploaded_at')
    list_display_links = ('id', 'thumbnail_preview', 'filename')
    list_filter = ('uploaded_at',)
    search_fields = ('filename', 'tags')
    list_per_page = 20

    def get_tags_display(self, obj):
        return ", ".join(obj.tags)
    get_tags_display.short_description = "Tags"