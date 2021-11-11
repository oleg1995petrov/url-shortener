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
        return redirect(shortener.long_url)
    
    try:
        shortener = Shortener.objects.get(short_url=short_url)
    except Shortener.DoesNotExist:
        raise Http404("Sorry, this link doesn't exist :(")
    else:
        shortener.times_followed = F('times_followed') + 1
        shortener.save()
        return redirect(shortener.long_url)


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
        link_form = AnonymousShortenerForm(data=request.POST)
        
        if link_form.is_valid():
            shortened_obj = link_form.save(commit=False)
            shortened_obj.ip = get_client_ip(request)
            shortened_obj.long_url = clean_shortened_obj(shortened_obj)
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

        menu = HIDDEN if request.GET.get('hidden') == 'true' else VISIBLE
        user_links = (request.user.links.all() if menu == VISIBLE else
                      request.user.links.filter(hidden=True))
        link_form = ShortenerForm()
        active_link_id = request.GET.get('id')

        try:
            active_link = Shortener.objects.get(user=request.user, 
                                                pk=active_link_id)
        except Shortener.DoesNotExist:
            active_link = None

        context = {
            'user_links': user_links,
            'endpoint': 'dashboard',
            'menu': menu,
            'link_form': link_form,
            'active_link': active_link
        }
        return render(request, 'dashboard.html', context)

    def post(self, request, *args, **kwargs):
        link_form = ShortenerForm(data=request.POST)
        
        if link_form.is_valid():
            shortened_obj = link_form.save(commit=False)
            shortened_obj.long_url = clean_shortened_obj(shortened_obj)
            shortened_obj.user = request.user
            shortened_obj.save()
        
        for error in link_form.errors:
            messages.error(request, link_form.errors[error])
        return redirect('shortener:dashboard')
