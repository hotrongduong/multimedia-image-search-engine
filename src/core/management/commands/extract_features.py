from django.core.management.base import BaseCommand
from core.models import CorelImage, ImageFeature
from core.manual_features import extract_color_hsv, extract_glcm, extract_sobel_grid
from django.conf import settings
import os
import time
import numpy as np

class Command(BaseCommand):
    help = 'Features Extraction (HSV, GLCM, Sobel)'

    def handle(self, *args, **options):
        images = CorelImage.objects.all()
        total = images.count()
        
        self.stdout.write(f"Starting to extract {total} images...") 
        for index, img_obj in enumerate(images):
            full_path = os.path.join(settings.MEDIA_ROOT, img_obj.relative_path) 
            if not os.path.exists(full_path):
                continue

            try:
                vec_color = extract_color_hsv(full_path)
                ImageFeature.objects.update_or_create(
                    image=img_obj, method='color_hsv',
                    defaults={'vector': vec_color.tolist(), 'dimension': len(vec_color)}
                )

                vec_glcm = extract_glcm(full_path)
                ImageFeature.objects.update_or_create(
                    image=img_obj, method='glcm',
                    defaults={'vector': vec_glcm.tolist(), 'dimension': len(vec_glcm)}
                )

                vec_sobel = extract_sobel_grid(full_path)
                ImageFeature.objects.update_or_create(
                    image=img_obj, method='sobel',
                    defaults={'vector': vec_sobel.tolist(), 'dimension': len(vec_sobel)}
                )

                vec_fused = np.concatenate([vec_color, vec_glcm, vec_sobel])
                ImageFeature.objects.update_or_create(
                    image=img_obj, method='fused',
                    defaults={'vector': vec_fused.tolist(), 'dimension': len(vec_fused)}
                )

                if (index + 1) % 100 == 0:
                    self.stdout.write(f"Tiến độ: {index + 1}/{total}")
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Lỗi {img_obj.filename}: {e}"))

        self.stdout.write(self.style.SUCCESS("Extracted Successfully!"))