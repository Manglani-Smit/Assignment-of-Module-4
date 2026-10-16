from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_view, name='index'),
    path('task1/', views.task1_view, name='task1'),
    path('api/song/<int:song_id>/', views.delete_song_api, name='delete_song'),
    path('task2/', views.task2_view, name='task2'),
    path('remove-wishlist/<int:item_id>/', views.remove_wishlist_api, name='remove_wishlist'),
    path('task3/', views.task3_view, name='task3'),
    path('api/movie/<int:movie_id>/', views.delete_movie_api, name='delete_movie'),
    path('task4/', views.task4_view, name='task4'),
    path('api/playlist/<int:playlist_id>/', views.delete_playlist_api, name='delete_playlist'),
]