from django import forms
from .models import AdComment

class AdCommentForm(forms.ModelForm):
    user_name = forms.CharField(required=False, widget=forms.TextInput(
        attrs={
            'id': 'inputName',
            'class': 'form-control form-control-lg form-control-a',
            'placeholder': 'Name *'

        }
    ))

    user_name_email = forms.EmailField(required=False, widget=forms.EmailInput(
        attrs={
            'class': 'form-control form-control-lg form-control-a',
            'id': 'inputEmail1',
            'placeholder': 'Email *'
        }
    ))

    message = forms.CharField(widget=forms.Textarea(
        attrs={
            'class': 'form-control',
            'id': 'textMessage',
            'placeholder': 'Comment *',
            'name': 'message',
            'cols': 45,
            'rows': 8
        }
    ))

    class Meta:
       model = AdComment
       fields = ['user_name', 'user_name_email', 'message']