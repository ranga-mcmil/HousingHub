from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import User
from django.forms import ClearableFileInput

ACCOUNT_TYPE =(
    ("ADVERTISER", "Advertiser"),
    ("TENANT", "Tenant"),
)

class CustomLoginForm(AuthenticationForm):

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.fields['username'].widget.attrs.update(
      {'class': 'form-control', }
    )
    self.fields['password'].widget.attrs.update(
      {'class': 'form-control', }
    )



class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Email / Phone Number')

class UserRegistrationForm(forms.ModelForm):

    first_name = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'name': 'first_name',
        }
    ))

    last_name = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'name': 'last_name',
        }
    ))

    user_type = forms.ChoiceField(choices=ACCOUNT_TYPE, widget=forms.Select(
        attrs={
            'class': 'form-control',
            'name': 'type',

        }
    ))

    email = forms.EmailField(widget=forms.EmailInput(
        attrs={
            'class': 'form-control',
            'name': 'email',
        }
    ))
    
    contact_number = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'name': 'contact_number',
        }
    ))

    pic = forms.ImageField(widget=forms.FileInput(
        attrs={
            'id':"file",
            'class': 'form-control image-input',
        }
    ))

    password = forms.CharField(label='Password', widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'name': 'password',
            'minlength': "8"
        }
    ))
    password2 = forms.CharField(label='Password', widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'name': 'password',
            'minlength': "8"
        }
    ))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'user_type', 'email', 'contact_number', 'pic', )

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords dont match')



class UserUpdateForm(forms.ModelForm):

    first_name = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'name': 'first_name',
        }
    ))

    last_name = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'name': 'last_name'
        }
    ))
    
    contact_number = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'name': 'contact_number'
        }
    ))

    bio = forms.CharField(widget=forms.Textarea(
        attrs={
            'class': 'form-control',
            'id': 'description',
            'placeholder': 'Bio *',
            'name': 'bio',
            'cols': 45,
            'rows': 8
        }
    ))

    pic = forms.ImageField(widget=forms.FileInput(
        attrs={
            'class': 'form-control image-input',
            'id':"file"
        }
    ))
    
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'contact_number', 'bio', 'pic')
