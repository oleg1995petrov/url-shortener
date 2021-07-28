from django import forms
from django.forms.utils import ErrorDict

from .models import Shortener
from .utils import check_long_url 


class ShortenerForm(forms.ModelForm):
    long_url = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "form-control form-control-md", 
                "placeholder": "Enter a long link here"
            }
        )
    )
    ip = forms.CharField(required=False)
       
    class Meta:
        model = Shortener
        fields = ('long_url', 'ip')

    def clean(self):
        cd = super().clean()
        long_url = cd.get('long_url', 'X')
        is_correct = check_long_url(long_url)
        if not is_correct:
            raise forms.ValidationError("Invalid link!")
