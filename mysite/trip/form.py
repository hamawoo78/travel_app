from django import forms
from .models import Location


class SearchForm(forms.ModelForm):
    destination = forms.CharField(label="")
    class Meta:
        model = Location 
        fields = ['destination',]