from django.shortcuts import render, redirect
from django.http import Http404
from django.views.generic import View
from django.contrib import messages
from django.db.models import F

from shortener.models import AnonymousShortener, Shortener
from shortener.forms import AnonymousShortenerForm, ShortenerForm
from shortener.services import get_client_ip, clean_shortened_obj
from users.forms import SignUpForm, SignInForm


def redirect_to(request, short_url):
    try:
        shortener = AnonymousShortener.objects.get(short_url=short_url)
    except AnonymousShortener.DoesNotExist:
        pass
    else:
        return redirect(shortener.get_long_url)
    
    try:
        shortener = Shortener.objects.get(short_url=short_url)
    except Shortener.DoesNotExist:
        raise Http404("Sorry, this link doesn't exist :(")
    else:
        shortener.times_followed = F('times_followed') + 1
        shortener.save()
        return redirect(shortener.get_long_url)


class AnonymousShortenerView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('shortener:dashboard')

        context = {
            'signin_form': SignInForm(),
            'signup_form': SignUpForm(),
            'link_form': AnonymousShortenerForm(),
            'urls': AnonymousShortener.objects.filter(
                ip=get_client_ip(request))[:3]
        }
        return render(request, 'home.html', context)

    def post(self, request, *args, **kwargs):
        link_form = AnonymousShortenerForm(request.POST)
        
        if link_form.is_valid():
            shortened_obj = link_form.save(commit=False)
            shortened_obj.ip = get_client_ip(request)
            shortened_obj.protocol, shortened_obj.long_url = (
                clean_shortened_obj(shortened_obj))
            shortened_obj.save()
            return redirect('shortener:home')
       
        for error in link_form.errors:
            messages.error(request, link_form.errors[error])
        return redirect('shortener:home')


class DashboardView(View):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('shortener:home')
        
        VISIBLE = 'visible'
        HIDDEN = 'hidden'
        ENDPOINT = 'dashboard'

        dashboard_menu = HIDDEN if request.GET.get('hidden') == 'true' else VISIBLE
        links = (Shortener.objects.filter(user=request.user) if dashboard_menu == VISIBLE 
                 else Shortener.objects.filter(user=request.user, hidden=True))
        link_form = ShortenerForm()
        chosen_link_id = request.GET.get('id')

        try:
            chosen_link = Shortener.objects.get(user=request.user, pk=chosen_link_id)
        except Shortener.DoesNotExist:
            chosen_link = None

        context = {
            'links': links,
            'endpoint': ENDPOINT,
            'dashboard_menu': dashboard_menu,
            'link_form': link_form,
            'chosen_link': chosen_link
        }
        return render(request, 'dashboard.html', context)

    def post(self, request, *args, **kwargs):
        link_form = ShortenerForm(request.POST)
        if link_form.is_valid():
            shortened_obj = link_form.save(commit=False)
            shortened_obj.protocol, shortened_obj.long_url = (
                clean_shortened_obj(shortened_obj))
            shortened_obj.user = request.user
            shortened_obj.save()
        
        for error in link_form.errors:
            messages.error(request, link_form.errors[error])
        return redirect('shortener:dashboard')
