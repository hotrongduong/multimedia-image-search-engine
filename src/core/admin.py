from django.contrib import admin
from django.utils.html import format_html
from .models import CorelImage, ImageFeature

@admin.register(CorelImage)
class CorelImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'image_preview', 'filename', 'image_info', 'display_labels', 'created_at')
    list_filter = ('format', 'mode')
    search_fields = ('filename', 'labels')
    list_per_page = 20

    def image_preview(self, obj):
        if obj.relative_path:
            image_url = f"/media/{obj.relative_path}"
            return format_html('<img src="{}" style="width: 120px; height: auto; border-radius: 4px; border: 1px solid #ccc;" />', image_url)
        return "No Image"
    image_preview.short_description = "Image Preview"

    def image_info(self, obj):
        return f"{obj.format} | {obj.width}x{obj.height}"
    image_info.short_description = "Image Info"

    def display_labels(self, obj):
        html = ""
        if obj.labels:
            for label in obj.labels[:5]:
                html += f'<span style="background-color: #e3f2fd; color: #1565c0; padding: 2px 6px; margin-right: 4px; border-radius: 4px; font-size: 11px;">{label}</span>'
        return format_html(html)
    display_labels.short_description = "Labels"

@admin.register(ImageFeature)
class ImageFeatureAdmin(admin.ModelAdmin):
    list_display = ('get_thumbnail', 'get_filename', 'method', 'dimension', 'vector_preview', 'created_at')
    list_filter = ('method',)
    search_fields = ('image__filename',)
    
    def get_thumbnail(self, obj):
        if obj.image.relative_path:
            image_url = f"/media/{obj.image.relative_path}"
            return format_html('<img src="{}" style="width: 80px; height: auto;" />', image_url)
        return "-"
    get_thumbnail.short_description = "Original Image"

    def get_filename(self, obj):
        return obj.image.filename
    get_filename.short_description = "Image Filename"

    def vector_preview(self, obj):
        if obj.vector:
            preview = [round(x, 4) for x in obj.vector[:5]]
            return f"{preview}..." 
        return "Empty"
    vector_preview.short_description = "Vector (Preview)"