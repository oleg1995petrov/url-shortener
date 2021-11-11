from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from django.views.generic import View

from users.forms import SignUpForm, SignInForm


class SignUpView(View):
    """
    Handles the sign up action.
    """
    def post(self, request, *args, **kwargs):
        signup_form = SignUpForm(data=request.POST)

        if signup_form.is_valid():
            user = signup_form.save()
            login(request, user)
        else:
            for error in signup_form.errors:
                messages.error(request, signup_form.errors[error])

        return redirect('shortener:dashboard')


class SignInView(View):
    """
    Handles the login action.
    """
    def post(self, request, *args, **kwargs):
        signin_form = SignInForm(data=request.POST)

        if signin_form.is_valid():
            user = signin_form.get_user()
            login(request, user)
        else:
            for error in signin_form.errors:
                messages.error(request, signin_form.errors[error])
            
        return redirect('shortener:dashboard')
