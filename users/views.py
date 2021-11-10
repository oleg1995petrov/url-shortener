from django.contrib import messages
from django.db import IntegrityError
from django.shortcuts import redirect
from django.views.generic import View
from django.contrib.auth import authenticate, login, logout
# from django.contrib.auth.views import LoginView

from users.forms import SignUpForm, SignInForm


class SignUpView(View):
    """ """
    def post(self, request, *args, **kwargs):
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)

        for error in form.errors:
            messages.error(request, form.errors[error])

        return redirect('shortener:home')


class SignInView(View):
    """ """
    def post(self, request, *args, **kwargs):
        form = SignInForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            username = cd['email']
            password = cd['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                # if user.is_active:
                login(request, user)

        for error in form.errors:
            messages.error(request, form.errors[error])
            
        return redirect('/')
