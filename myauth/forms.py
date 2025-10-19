from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


class RegisterForm(forms.Form):
    username = forms.CharField(max_length=20, widget=forms.TextInput(attrs={
        'placeholder': 'Login',
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Password',
    }), label="Пароль")
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'placeholder': 'Email',
    }))

class LoginForm(forms.Form):
    username = forms.CharField(max_length=20, widget=forms.TextInput(attrs={
            'placeholder': 'Login',
        }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Password',
    }), label="Пароль")
