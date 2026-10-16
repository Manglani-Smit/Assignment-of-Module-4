from django.contrib import admin
from .models import User, Order, Product, MovieReview, Playlist

# User model registration
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'fname', 'lname', 'email', 'mobile', 'usertype', 'group_name')
    search_fields = ('fname', 'email', 'mobile')
    list_filter = ('usertype', 'group_name')

# Q1: Order admin
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'restaurant_name', 'user', 'total_amount', 'order_date')

# Q2: Product admin
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'product_name', 'seller', 'price', 'created_at')

# Q3: Movie Review admin
@admin.register(MovieReview)
class MovieReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'movie_name', 'user', 'rating')

# Q5: Playlist model admin (Sirf Admin group walo ke liye restricted)
@admin.register(Playlist)
class PlaylistAdmin(admin.ModelAdmin):
    list_display = ('id', 'playlist_name', 'user', 'total_songs', 'created_date')

    # Django admin me permission check karna
    def has_module_permission(self, request):
        # Superuser ke liye open ya agar session me group 'Admin' ho
        if request.user.is_superuser:
            return True
        return request.user.groups.filter(name='Admin').exists()

    def has_view_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return request.user.groups.filter(name='Admin').exists()

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return request.user.groups.filter(name='Admin').exists()

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return request.user.groups.filter(name='Admin').exists()

    def has_add_permission(self, request):
        if request.user.is_superuser:
            return True
        return request.user.groups.filter(name='Admin').exists()