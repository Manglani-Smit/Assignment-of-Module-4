from django.contrib import admin
from .models import *
# Register your models here.
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('name', 'cuisine', 'rating')
    search_fields = ('name', 'cuisine')

admin.site.register(Restaurant, RestaurantAdmin)