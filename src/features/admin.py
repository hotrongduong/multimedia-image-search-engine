from django.contrib import admin
from django.utils.html import mark_safe
from .models import FeatureColor, FeatureTexture, FeatureShape, FeatureSemantic

def get_image_preview(obj):
    if obj.image:
        return obj.image.thumbnail_preview()
    return "No Image"

def format_vector(vector_data, precision=4):
    if not vector_data:
        return "Empty"
    preview = vector_data[:5]
    
    if isinstance(preview[0], float):
        preview_str = ", ".join([f"{x:.{precision}f}" for x in preview])
    else:
        preview_str = ", ".join([str(x) for x in preview])
        
    return f"[{preview_str}, ...] ({len(vector_data)} dims)"

@admin.register(FeatureColor)
class FeatureColorAdmin(admin.ModelAdmin):
    list_display = ('id', 'image_thumbnail', 'image_filename', 'short_histogram', 'created_at')
    list_display_links = ('id', 'image_filename')
    search_fields = ('image__filename',)

    def image_thumbnail(self, obj):
        return get_image_preview(obj)
    image_thumbnail.short_description = "Original Image"

    def image_filename(self, obj):
        return obj.image.filename
    image_filename.short_description = "Fine Name"

    def short_histogram(self, obj):
        return format_vector(obj.histogram)
    short_histogram.short_description = "Color Vector (HSV)"


@admin.register(FeatureTexture)
class FeatureTextureAdmin(admin.ModelAdmin):
    list_display = ('id', 'image_thumbnail', 'image_filename', 'short_lbp', 'created_at')
    
    def image_thumbnail(self, obj):
        return get_image_preview(obj)
    image_thumbnail.short_description = "Original Image"

    def image_filename(self, obj):
        return obj.image.filename

    def short_lbp(self, obj):
        return format_vector(obj.lbp_histogram)
    short_lbp.short_description = "Texture Vector (LBP)"


@admin.register(FeatureShape)
class FeatureShapeAdmin(admin.ModelAdmin):
    list_display = ('id', 'image_thumbnail', 'image_filename', 'short_hog', 'created_at')

    def image_thumbnail(self, obj):
        return get_image_preview(obj)
    image_thumbnail.short_description = "Original Image"

    def image_filename(self, obj):
        return obj.image.filename

    def short_hog(self, obj):
        return format_vector(obj.hog_vector)
    short_hog.short_description = "Shape Vector (HOG)"


@admin.register(FeatureSemantic)
class FeatureSemanticAdmin(admin.ModelAdmin):
    list_display = ('id', 'image_thumbnail', 'image_filename', 'short_embedding', 'created_at')

    def image_thumbnail(self, obj):
        return get_image_preview(obj)
    image_thumbnail.short_description = "Original Image"

    def image_filename(self, obj):
        return obj.image.filename

    def short_embedding(self, obj):
        data = list(obj.embedding) if obj.embedding is not None else []
        return format_vector(data)
    short_embedding.short_description = "Vector AI (ResNet50)"