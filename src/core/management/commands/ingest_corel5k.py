import os
import json
from django.core.management.base import BaseCommand
from django.core.files import File
from core.models import ImageMetadata

class Command(BaseCommand):
    help = 'Ingest Corel-5k dataset into Database.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--path', 
            type=str, 
            default='/app/data/Corel-5k',
            help='Corel-5k dataset folder path.'
        )

    def handle(self, *args, **options):
        base_path = options['path']
        img_dir = os.path.join(base_path, 'images')
        
        target_files = ['train.json', 'test.json']
        self.stdout.write(self.style.WARNING(f"Starting scan data in: {base_path}"))
        if not os.path.exists(img_dir):
            self.stdout.write(self.style.ERROR(f"Images folder not found: {img_dir}"))
            return

        total_added = 0
        total_skipped = 0
        for json_file in target_files:
            file_path = os.path.join(base_path, json_file)
            if not os.path.exists(file_path):
                self.stdout.write(self.style.ERROR(f"File not found: {json_file}"))
                continue

            self.stdout.write(f"--> Reading file: {json_file}...")
            with open(file_path, 'r') as f:
                try:
                    data = json.load(f)
                    samples = data.get('samples', [])
                except json.JSONDecodeError:
                    self.stdout.write(self.style.ERROR(f"[ERROR] Reading JSON: {json_file}"))
                    continue

            for item in samples:
                img_name = item['image_name']    
                labels = item['image_labels']    
                if ImageMetadata.objects.filter(filename=img_name).exists():
                    total_skipped += 1
                    continue

                phys_path = os.path.join(img_dir, img_name)
                if not os.path.exists(phys_path):
                    self.stdout.write(self.style.WARNING(f"[SKIPPING]: Image file not found: {img_name}"))
                    continue

                try:
                    with open(phys_path, 'rb') as f_img:
                        metadata = ImageMetadata(
                            filename=img_name,
                            tags=labels
                        )
                        metadata.image_file.save(img_name, File(f_img), save=True)
                        total_added += 1
                        
                        if total_added % 100 == 0:
                            self.stdout.write('.', ending='')
                            self.stdout.flush()
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"\nSAVE ERROR {img_name}: {e}"))

        self.stdout.write(self.style.SUCCESS(
            f"\n\nSUCCESSFULLY!"
            f"\n- Number of new images: {total_added} iamges"
            f"\n- Number of errors: {total_skipped} images"
        ))