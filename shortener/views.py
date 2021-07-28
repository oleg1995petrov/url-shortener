import re

from django.shortcuts import render, redirect
from django.http import Http404
from django.views.generic import View
from django.contrib import messages
from django.db.models import F


from .models import Shortener
from .forms import ShortenerForm
from .utils import check_long_url, get_client_ip


class ShortenerView(View):
    def get(self, request, *args, **kwargs):
        context = {}
        context['form'] = ShortenerForm()
        context['urls'] = Shortener.objects.filter(ip=get_client_ip(request))[:5]
        return render(request, 'home.html', context)
    def post(self, request, *args, **kwargs):
        form = ShortenerForm(request.POST)
        
        if form.is_valid():
            long_url = form.cleaned_data['long_url'].strip()
            is_correct = check_long_url(long_url)

            if is_correct:
                shortened_object = form.save()
                shortened_object.ip = get_client_ip(request)
                shortened_object.save(update_fields=['ip'])
                return redirect('home')

        for error in form.errors:
            messages.error(request, form.errors[error])
        return redirect('home')


def redirect_to(request, short_url):
    try:
        shortener = Shortener.objects.get(short_url=short_url)   
        shortener.times_followed = F('times_followed') + 1       
        shortener.save()
        return redirect(
            shortener.long_url if shortener.long_url[:4] == 'http' else 
            f'http://{shortener.long_url}'
        )
    except:
        raise Http404('Sorry this link is broken :(')