from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

def index_view(request):
    return render(request, 'index.html')

def task1_view(request):
    return render(request, 'task1.html')

@csrf_exempt
def delete_song_api(request, song_id):
    if request.method == 'DELETE':
        return JsonResponse({'status': 'success', 'message': f'Song {song_id} deleted'})
    return JsonResponse({'error': 'Invalid method'}, status=400)

def task2_view(request):
    return render(request, 'task2.html')

@csrf_exempt
def remove_wishlist_api(request, item_id):
    if request.method == 'DELETE':
        return JsonResponse({'status': 'success', 'deleted_id': item_id})
    return JsonResponse({'error': 'Invalid method'}, status=400)

def task3_view(request):
    return render(request, 'task3.html')

@csrf_exempt
def delete_movie_api(request, movie_id):
    if request.method == 'DELETE':
        return JsonResponse({'status': 'success', 'message': 'Movie removed successfully'})
    return JsonResponse({'error': 'Invalid method'}, status=400)

def task4_view(request):
    return render(request, 'task4.html')

@csrf_exempt
def delete_playlist_api(request, playlist_id):
    if request.method == 'DELETE':
        return JsonResponse({'status': 'success', 'message': f'Playlist {playlist_id} deleted'})
    return JsonResponse({'error': 'Invalid method'}, status=400)