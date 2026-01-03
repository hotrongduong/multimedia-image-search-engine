from django.core.management.base import BaseCommand
from core.models import ImageMetadata
from features.models import FeatureColor, FeatureTexture, FeatureShape, FeatureSemantic

from features.extractors.color import extract_color_histogram
from features.extractors.texture import extract_texture_lbp
from features.extractors.shape import extract_shape_hog
from features.extractors.semantic import SemanticExtractor

class Command(BaseCommand):
    help = 'Extract features for all images in Database'

    def handle(self, *args, **options):
        images = ImageMetadata.objects.all().order_by('id')
        total = images.count()
        self.stdout.write(f"found {total} images. Starting process...")

        semantic_model = SemanticExtractor()

        count = 0
        for img_obj in images:
            count += 1
            if count % 10 == 0:
                self.stdout.write(f"Processing {count}/{total}...")

            img_path = img_obj.image_file.path

            if not hasattr(img_obj, 'color_feature'):
                vec_color = extract_color_histogram(img_path)
                FeatureColor.objects.create(image=img_obj, histogram=vec_color)

            if not hasattr(img_obj, 'texture_feature'):
                vec_texture = extract_texture_lbp(img_path)
                FeatureTexture.objects.create(image=img_obj, lbp_histogram=vec_texture)

            if not hasattr(img_obj, 'shape_feature'):
                vec_shape = extract_shape_hog(img_path)
                if vec_shape:
                    FeatureShape.objects.create(image=img_obj, hog_vector=vec_shape)

            if not hasattr(img_obj, 'semantic_feature'):
                vec_semantic = semantic_model.extract(img_path)
                FeatureSemantic.objects.create(image=img_obj, embedding=vec_semantic)

        self.stdout.write(self.style.SUCCESS("Extracted Features Sucessfully!"))