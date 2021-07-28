from django.urls import path

from . import views


urlpatterns = [
    path('<str:short_url>', views.redirect_to),
    path('', views.ShortenerView.as_view(), name='home'),
]
