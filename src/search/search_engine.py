from features.models import FeatureColor, FeatureTexture, FeatureShape, FeatureSemantic
from .metrics import chi2_distance, euclidean_distance
from pgvector.django import CosineDistance

class SearchEngine:
    def __init__(self):
        pass

    def _convert_dist_to_score(self, dist):
        return 1.0 / (1.0 + dist)

    def search_by_color(self, query_hist, top_k=15):
        results = []
        features = FeatureColor.objects.select_related('image').all()
        
        for f in features:
            dist = chi2_distance(query_hist, f.histogram)
            score = self._convert_dist_to_score(dist)
            results.append((f.image, score))
        
        results.sort(key=lambda x: x[1], reverse=True)
        return results[:top_k]

    def search_by_texture(self, query_lbp, top_k=15):
        results = []
        features = FeatureTexture.objects.select_related('image').all()
        
        for f in features:
            dist = chi2_distance(query_lbp, f.lbp_histogram)
            score = self._convert_dist_to_score(dist)
            results.append((f.image, score))
            
        results.sort(key=lambda x: x[1], reverse=True)
        return results[:top_k]

    def search_by_shape(self, query_hog, top_k=15):
        results = []
        features = FeatureShape.objects.select_related('image').all()
        
        for f in features:
            dist = euclidean_distance(query_hog, f.hog_vector)
            score = self._convert_dist_to_score(dist)
            results.append((f.image, score))
            
        results.sort(key=lambda x: x[1], reverse=True)
        return results[:top_k]

    def search_by_semantic(self, query_embedding, top_k=15):
        db_results = FeatureSemantic.objects.annotate(
            distance=CosineDistance('embedding', query_embedding)
        ).order_by('distance')[:top_k]
        
        results = []
        for r in db_results:
            score = 1.0 - r.distance
            results.append((r.image, score))
            
        results.sort(key=lambda x: x[1], reverse=True)
        return results