from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django import forms


class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=254)
    password = forms.CharField(label="Password", widget=forms.PasswordInput)
    username = forms.CharField(
        max_length=254,
        widget=forms.TextInput(attrs={
            'class': 'form-control', 'placeholder': 'Username', 'required': 'True',
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control', 'placeholder': 'Password', 'required': 'True',
        })
    )
