from django.shortcuts import render, get_object_or_404
from .models import Playlist

def playlist_list(request):
    playlists = Playlist.objects.all().order_by('-created_at')
    return render(request, 'playlist_list.html', {'playlists': playlists})

def playlist_detail(request, pk):
    playlist = get_object_or_404(Playlist, pk=pk)
    return render(request, 'playlist_detail.html', {'playlist': playlist})