from django.urls import path
from django.contrib.auth.views import LogoutView
from users.views import SignUpView, SignInView


app_name = 'users'


urlpatterns = [
    path('signin/', SignInView.as_view(), name='signin'),
    path('signout/', LogoutView.as_view(), name='signout'),
    path('signup/', SignUpView.as_view(), name='signup'),

]
