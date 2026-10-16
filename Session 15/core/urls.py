from django.urls import path
from . import views

urlpatterns = [
    path('my-orders/', views.my_orders, name='my_orders'),
    path('post-product/', views.post_product, name='post_product'),
    path('movie-reviews/', views.movie_reviews, name='movie_reviews'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('seller-dashboard/', views.seller_dashboard, name='seller_dashboard'),
    path('buyer-dashboard/', views.buyer_dashboard, name='buyer_dashboard'),
    path('playlists/', views.playlist_view, name='playlists'),
    path('test-login/<str:email>/', views.test_login, name='test_login'),
]