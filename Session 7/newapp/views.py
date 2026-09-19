from django.shortcuts import render
from .models import *
# Create your views here.

def add_restaurant(request):
    if request.method == 'POST':
        if len(request.POST['name']) < 3:
            msg = "Name Should be greater than 3"
            return render(request, 'add_restaurant.html', {'msg': msg})

        rating = float(request.POST['rating'])
        if rating < 1 or rating > 5:
            msg = "Rating must be between 1 and 5"
            return render(request, 'add_restaurant.html', {'msg': msg})

        try:
            Restaurant.objects.create(
                name=request.POST['name'],
                cuisine=request.POST['cuisine'],
                rating=request.POST['rating'],
            )
            msg = "Restaurant added successfully"
            return render(request, 'add_restaurant.html', {'msg': msg})
        except:
            msg = "Restaurant already exists"
            return render(request, 'add_restaurant.html', {'msg': msg})

    else:
        return render(request, 'add_restaurant.html')