from django import forms
# from django.forms.utils import ErrorDict
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


class SignUpForm(UserCreationForm):
    """
    A form that creates a user, with no privileges, 
    from the given email and password.
    """
    class Meta:
        model = get_user_model()
        fields = ('email',)

    email = forms.EmailField(
        label='',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Email',
                'class': 'form-control'
            }
        )
    )
    password1 = forms.CharField(
        label='',
        min_length=8,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Password',
                'class': 'form-control'
            }
        )
    )
    password2 = forms.CharField(
        label='',
        min_length=8,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Password again',
                'class': 'form-control'
            }
        )
    )


class SignInForm(AuthenticationForm):
    """
    A form to authenticate users.
    """
    username = forms.EmailField(
        label='',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Email',
                'class': 'form-control'
            }
        )
    )
    password = forms.CharField(
        label='',
        min_length=8,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Password',
                'class': 'form-control'
            }
        )
    )
