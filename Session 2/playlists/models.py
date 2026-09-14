from django.db import models
from django.http import HttpResponse
# Create your models here.

def home(request):
    return HttpResponse("Welcome to My Spotify Playlists!")
