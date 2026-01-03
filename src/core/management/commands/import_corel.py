import os
import json
from PIL import Image
from django.core.management.base import BaseCommand
from django.conf import settings
from core.models import CorelImage

class Command(BaseCommand):
    help = "Import Corel-5K image data from JSON file into Database"

    def handle(self, *args, **options):
        BASE_DATA_DIR = os.path.join(settings.MEDIA_ROOT, 'corel5k')
        IMAGE_DIR = os.path.join(BASE_DATA_DIR, 'images')
        json_files = ['train.json', 'test.json']

        total_imported = 0
        total_error = 0

        self.stdout.write(self.style.WARNING(f"Starting to scan data at: {BASE_DATA_DIR}"))
        for json_file in json_files:
            file_path = os.path.join(BASE_DATA_DIR, json_file)
            if not os.path.exists(file_path):
                self.stdout.write(self.style.ERROR(f"File not found: {file_path}"))
                continue

            self.stdout.write(f"Reading file: {json_file}")
            try:
                with open(file_path, 'r') as f:
                    data = json.load(f)

                    items = data.get('samples', []) if isinstance(data, dict) else data
                    for item in items:
                        filename = item.get('image_name')
                        labels = item.get('image_labels', [])

                        image_path_real = os.path.join(IMAGE_DIR, filename)
                        if not os.path.exists(image_path_real):
                            self.stdout.write(self.style.ERROR(f"MISSING Image: {filename}"))
                            total_error += 1
                            continue

                        try:
                            with Image.open(image_path_real) as img:
                                width, height = img.size
                                fmt = img.format or 'JPEG'
                                mode = img.mode
                        except Exception as e:
                            self.stdout.write(self.style.ERROR(f'ERROR reading image {filename}: {str(e)}'))
                            total_error += 1
                            continue

                        rel_path = os.path.join("corel5k/images", filename)
                        obj, created = CorelImage.objects.update_or_create(
                            filename=filename,
                            defaults={
                                'relative_path': rel_path,
                                'width': width,
                                'height': height,
                                'format': fmt,
                                'mode': mode,
                                'labels': labels,
                            }
                        )

                        if created:
                            total_imported += 1
                            if total_imported % 100 == 0:
                                self.stdout.write('.', ending='')
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"ERROR while reading JSON {json_file}: {str(e)}"))
        
        self.stdout.write(self.style.SUCCESS(f'\n\nFINISH!'))
        self.stdout.write(self.style.SUCCESS(f'- Total images imported: {total_imported} images'))
        self.stdout.write(self.style.ERROR(f'- Error/missing images: {total_error} images'))