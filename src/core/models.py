from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.utils.html import mark_safe

class CorelImage(models.Model):
    filename = models.CharField(max_length=255, unique=True, verbose_name="File Name")
    relative_path = models.CharField(max_length=500, verbose_name="Relative Path")
    width = models.IntegerField(default=0, verbose_name="Width (px)")
    height = models.IntegerField(default=0, verbose_name="Height (px)")
    format = models.CharField(max_length=50, blank=True, verbose_name="Image Format")
    mode = models.CharField(max_length=50, blank=True, verbose_name="Color Mode")
    labels = ArrayField(models.CharField(max_length=100), blank=True, default=list, verbose_name="Labels")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")

    class Meta:
        verbose_name = "Corel-5K Image"
        verbose_name_plural = "Corel-5K Images"

    def __str__(self):
        return self.filename
    
    def image_preview(self):
        if self.relative_path:
            return mark_safe(f'<img src="{self.relative_path}" width="100" />')
        return "No Image"
    image_preview.short_description = "Image Preview"

class ImageFeature(models.Model):
    FEATURE_TYPES = [
        ('color_histogram', 'Color Histogram (HSV)'),
        ('glcm', 'Gray Level Co-occurrence Matrix (GLCM)'),
        ('sobel', 'Sobel Edge Detection'),
        ('fused', 'Fused Features'),
    ]
    image = models.ForeignKey(CorelImage, on_delete=models.CASCADE, related_name='features')
    method = models.CharField(max_length=50, choices=FEATURE_TYPES, verbose_name="Feature Extraction Method")
    vector = ArrayField(models.FloatField(), verbose_name="Feature Vector")
    dimension = models.IntegerField(verbose_name="Feature Dimension")
    extraction_time = models.FloatField(default=0.0, verbose_name="Extraction Time (seconds)")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Image Feature"
        verbose_name_plural = "Image Features"
        unique_together = ('image', 'method')

    def __str__(self):
        return f"{self.image.filename} - {self.method}"