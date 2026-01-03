from django.db import models
from django.contrib.auth.models import User
from django.utils.html import mark_safe

class UploadedImage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='uploaded_images')
    image = models.ImageField(upload_to='user_uploads/%Y/%m/%d/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-uploaded_at']

    def __str__(self):
        return f"Image {self.id} by {self.user.username}"

    def image_preview(self):
        if self.image:
            return mark_safe(f'<img src="{self.image.url}" style="height: 100px; border-radius: 5px; border: 1px solid #ddd;" />')
        return "No Image"

class SearchQuery(models.Model):
    METHOD_CHOICES = [
        ('color_hsv', 'Color HSV'),
        ('glcm', 'Texture GLCM'),
        ('sobel', 'Shape Sobel'),
        ('fused', 'Fused'),
    ]
    uploaded_image = models.ForeignKey(UploadedImage, on_delete=models.CASCADE, related_name='queries')
    method = models.CharField(max_length=50, choices=METHOD_CHOICES, default='fused')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Query {self.id} - {self.method}"

    def get_thumbnail(self):
        return self.uploaded_image.image_preview()