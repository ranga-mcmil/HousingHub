from django import forms
from .models import Ad
from .utils import CATEGORIES

class AdForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'id': 'product_name',
            'placeholder': 'Title *',
        }
    ))

    description = forms.CharField(widget=forms.Textarea(
        attrs={
            'class': 'form-control',
            'id': 'description',
            'placeholder': 'Description *',
            'name': 'message',
            'cols': 45,
            'rows': 8
        }
    ))

    category = forms.ChoiceField(choices=CATEGORIES, widget=forms.Select(
        attrs={
            'class': 'form-control',
            'name': 'category',
            'placeholder': 'What are you joining as: '

        }
    ))

    image = forms.ImageField(widget=forms.FileInput(
        attrs={
            'id': 'image',
            'class': 'form-control image-input',
        }
    ))

    class Meta:
       model = Ad
       fields = ['title', 'image', 'description', 'category']