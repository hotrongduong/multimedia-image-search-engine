from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import SearchForm
from .models import SearchQuery
from .utils import Searcher
from core.models import CorelImage

@login_required(login_url='/admin/login/')
def index(request):
    results = []
    query_image_url = None
    
    if request.method == 'POST':
        form = SearchForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_img = form.save(commit=False)
            uploaded_img.user = request.user
            uploaded_img.save()
            
            query_image_url = uploaded_img.image.url
            method = form.cleaned_data['method']

            SearchQuery.objects.create(
                uploaded_image=uploaded_img,
                method=method
            )

            searcher = Searcher(method)
            raw_results = searcher.search(uploaded_img, limit=12) # Top 12 for grid 4x3

            if raw_results:
                ids = [r['image_id'] for r in raw_results]
                corel_map = CorelImage.objects.in_bulk(ids)
                
                for r in raw_results:
                    img_obj = corel_map.get(r['image_id'])
                    if img_obj:
                        results.append({
                            'object': img_obj,
                            'score': round(r['score'], 4),
                            'percentage': round(r['score'] * 100, 1),
                            'labels': img_obj.labels
                        })
    else:
        form = SearchForm()

    return render(request, 'search_engine/index.html', {
        'form': form,
        'results': results,
        'query_image_url': query_image_url,
        'active_tab': 'home'
    })

@login_required(login_url='/admin/login/')
def history(request):
    # Get history logs for current user only
    logs = SearchQuery.objects.filter(uploaded_image__user=request.user).select_related('uploaded_image').order_by('-created_at')[:50]
    
    return render(request, 'search_engine/history.html', {
        'logs': logs,
        'active_tab': 'history'
    })