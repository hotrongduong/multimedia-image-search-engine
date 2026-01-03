from django.shortcuts import render
from django.conf import settings
import os

from features.extractors.color import extract_color_histogram
from features.extractors.texture import extract_texture_lbp
from features.extractors.shape import extract_shape_hog
from features.extractors.semantic import SemanticExtractor
from .search_engine import SearchEngine
from .models import SearchQuery

engine = SearchEngine()
semantic_model = SemanticExtractor() 

def index(request):
    return render(request, 'search/index.html')

def search_handler(request):
    if request.method == 'POST':
        file_path = None
        img_url = None
        method = request.POST.get('search_method', 'semantic')
        
        if request.FILES.get('query_img'):
            query_img = request.FILES['query_img']
            query_log = SearchQuery.objects.create(
                image=query_img,
                method=method
            )
            file_path = query_log.image.path
            img_url = query_log.image.url
            
        elif request.POST.get('current_image_path'):
            relative_path = request.POST.get('current_image_path')
            img_url = relative_path
            clean_path = relative_path.replace(settings.MEDIA_URL, '')
            file_path = os.path.join(settings.MEDIA_ROOT, clean_path)
        else:
            return render(request, 'search/index.html')

        results = []
        
        try:
            if file_path and os.path.exists(file_path):
                if method == 'color':
                    query_vec = extract_color_histogram(file_path)
                    results = engine.search_by_color(query_vec, top_k=15)
                
                elif method == 'texture':
                    query_vec = extract_texture_lbp(file_path)
                    results = engine.search_by_texture(query_vec, top_k=15)
                    
                elif method == 'shape':
                    query_vec = extract_shape_hog(file_path)
                    results = engine.search_by_shape(query_vec, top_k=15)
                    
                elif method == 'semantic':
                    query_vec = semantic_model.extract(file_path)
                    results = engine.search_by_semantic(query_vec, top_k=15)
            else:
                print(f"File not found: {file_path}")
                
        except Exception as e:
            print(f"Error searching: {e}")

        return render(request, 'search/index.html', {
            'results': results,
            'query_url': img_url,     
            'selected_method': method
        })

    return render(request, 'search/index.html')