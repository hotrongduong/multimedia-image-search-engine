from django import forms
from .models import UploadedImage, SearchQuery

class SearchForm(forms.ModelForm):
    method = forms.ChoiceField(choices=SearchQuery.METHOD_CHOICES, label="Search Method")

    class Meta:
        model = UploadedImage
        fields = ['image']