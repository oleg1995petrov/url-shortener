from django import forms
# from django.forms.utils import ErrorDict

from shortener.models import AnonymousShortener, Shortener
from shortener.services import check_long_url


class AnonymousShortenerForm(forms.ModelForm):
    """
    Shortener form for anonymous users.
    """
    class Meta:
        model = AnonymousShortener
        fields = ('long_url',)

    long_url = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control form-control", 
                "placeholder": "Enter a long link here"
            }
        )
    )

    def clean(self):
        cd = super().clean()
        long_url = cd.get('long_url')
        is_correct = check_long_url(long_url)
        if not is_correct:
            raise forms.ValidationError("Invalid URL!")


class ShortenerForm(AnonymousShortenerForm):
    """
    Shortener form for authenticated users.
    """
    class Meta:
        model = Shortener
        fields = ('long_url',)
