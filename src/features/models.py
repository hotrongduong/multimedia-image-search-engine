from django.db import models
from django.contrib.postgres.fields import ArrayField
from pgvector.django import VectorField
from core.models import ImageMetadata

class FeatureColor(models.Model):
    image = models.OneToOneField(ImageMetadata, on_delete=models.CASCADE, related_name='color_feature')
    histogram = ArrayField(models.IntegerField(), help_text="HSV Histogram Vector")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Color Feature for {self.image.filename}"

class FeatureTexture(models.Model):
    image = models.OneToOneField(ImageMetadata, on_delete=models.CASCADE, related_name='texture_feature')
    lbp_histogram = ArrayField(models.FloatField(), help_text="LBP Histogram Vector")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Texture Feature for {self.image.filename}"

class FeatureShape(models.Model):
    image = models.OneToOneField(ImageMetadata, on_delete=models.CASCADE, related_name='shape_feature')
    hog_vector = ArrayField(models.FloatField(), help_text="HOG Vector")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Shape Feature for {self.image.filename}"

class FeatureSemantic(models.Model):
    image = models.OneToOneField(ImageMetadata, on_delete=models.CASCADE, related_name='semantic_feature')
    embedding = VectorField(dimensions=2048, help_text="ResNet50 Embedding")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Semantic Feature for {self.image.filename}"