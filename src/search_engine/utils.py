import numpy as np
import os
from django.conf import settings
from core.models import ImageFeature
from core.manual_features import extract_color_hsv, extract_glcm, extract_sobel_grid

class Searcher:
    def __init__(self, method):
        self.method = method
        features = ImageFeature.objects.filter(method=method)
        
        self.ids = []
        self.vectors = []
        
        valid_features = [f for f in features if f.vector and len(f.vector) > 0]
        if valid_features:
            self.ids = [f.image.id for f in valid_features]
            self.vectors = np.array([f.vector for f in valid_features])

    def search(self, uploaded_image_obj, limit=20):
        if len(self.vectors) == 0:
            return []

        full_path = os.path.join(settings.MEDIA_ROOT, uploaded_image_obj.image.name)
        if not os.path.exists(full_path):
            return []

        try:
            query_vector = self._extract_feature(full_path)
            query_vec_np = np.array(query_vector)
            if query_vec_np.shape[0] != self.vectors.shape[1]:
                return []         
        except Exception:
            return []

        dists = np.linalg.norm(self.vectors - query_vec_np, axis=1)
        nearest_indices = np.argsort(dists)[:limit]

        results = []
        for idx in nearest_indices:
            image_id = self.ids[idx]
            distance = dists[idx]
            score = 1 / (1 + distance)
            
            results.append({
                'image_id': image_id,
                'score': score,
                'distance': distance
            })
            
        return results

    def _extract_feature(self, path):
        if self.method == 'color_hsv':
            return extract_color_hsv(path)
        elif self.method == 'glcm':
            return extract_glcm(path)
        elif self.method == 'sobel':
            return extract_sobel_grid(path)
        elif self.method == 'fused':
            v1 = extract_color_hsv(path)
            v2 = extract_glcm(path)
            v3 = extract_sobel_grid(path)
            return np.concatenate([v1, v2, v3])
        return []