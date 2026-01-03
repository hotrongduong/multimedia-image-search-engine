from django.db import models
from django.utils.html import mark_safe

class SearchQuery(models.Model):
    image = models.ImageField(upload_to='queries/%Y/%m/%d/', help_text="Ảnh người dùng upload")
    method = models.CharField(max_length=50, default='semantic')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Query {self.id} - {self.method} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"

    def thumbnail_preview(self):
        if self.image:
            return mark_safe(f'<img src="{self.image.url}" width="100" style="border-radius: 5px;" />')
        return "No Image"
    
    thumbnail_preview.short_description = "Ảnh truy vấn"