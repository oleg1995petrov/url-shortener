from django import forms
from django.forms.utils import ErrorDict
from django.conf import settings
from django.contrib.auth import password_validation, get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


class SignUpForm(UserCreationForm):
    """ """
    class Meta:
        model = get_user_model()
        fields = ('email',)

    email = forms.EmailField(
        label='',
        widget=forms.TextInput(
            attrs={'placeholder': 'Email',
                   'class': 'form-control'}
        )
    )
    password1 = forms.CharField(
        label='',
        min_length=8,
        widget=forms.PasswordInput(
            attrs={'placeholder': 'Password',
                   'class': 'form-control'}
        )
    )
    password2 = forms.CharField(
        label='',
        min_length=8,
        widget=forms.PasswordInput(
            attrs={'placeholder': 'Password again',
                   'class': 'form-control'}
        )
    )


class SignInForm(forms.Form):
    """ """
    email = forms.EmailField(
        label='',
        widget=forms.TextInput(
            attrs={'placeholder': 'Email',
                   'class': 'form-control'}
        )
    )
    password = forms.CharField(
        label='',
        min_length=8,
        widget=forms.PasswordInput(
            attrs={'placeholder': 'Password',
                   'class': 'form-control'
            }
        )
    )
