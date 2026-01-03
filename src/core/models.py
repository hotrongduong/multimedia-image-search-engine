from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.utils.html import mark_safe

class ImageMetadata(models.Model):
    filename = models.CharField(max_length=255, unique=True, help_text="Original file name.")
    image_file = models.ImageField(upload_to='corel5k_images/', help_text="Physical image file.")
    tags = ArrayField(
        models.CharField(max_length=100),
        blank=True,
        default=list,
        help_text="List of Labels."
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.filename
    
    def thumbnail_preview(self):
        if self.image_file:
            return mark_safe(f'<img src="{self.image_file.url}" width="100" style="border-radius: 5px;" />')
        return "No Image to display"
    
    thumbnail_preview.short_description = "Preview"