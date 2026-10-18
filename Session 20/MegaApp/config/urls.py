"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from core import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home_dashboard, name='home_dashboard'),
    path('restaurants/', views.search_restaurants, name='search_restaurants'),
    path('movie/register/', views.movie_register, name='movie_register'),
    path('movie/login/', views.movie_login, name='movie_login'),
    path('movie/verify-otp/', views.movie_verify_otp, name='movie_verify_otp'),
    path('movie/dashboard/', views.movie_dashboard, name='movie_dashboard'),
    path('logout/', views.user_logout, name='user_logout'),
    path('profile/', views.flipkart_profile, name='flipkart_profile'),
    path('cab-booking/', views.cab_booking_map, name='cab_booking_map'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)