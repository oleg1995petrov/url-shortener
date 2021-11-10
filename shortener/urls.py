from django.urls import path

from shortener import views


app_name = 'shortener'


urlpatterns = [
    path('', views.AnonymousShortenerView.as_view(), name='home'),
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    
    path('<str:short_url>/', views.redirect_to),
]
