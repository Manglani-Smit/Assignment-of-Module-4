from django.shortcuts import render
from django.conf import settings
from .utils import get_coordinates, haversine_distance, find_nearby_cafes

PICKUP_POINTS = [
    {"name": "Flipkart Hub - Navrangpura", "address": "Navrangpura, Ahmedabad", "lat": 23.0365, "lng": 72.5611},
    {"name": "Flipkart Hub - Satellite", "address": "Satellite, Ahmedabad", "lat": 23.0304, "lng": 72.5178},
    {"name": "Flipkart Hub - Maninagar", "address": "Maninagar, Ahmedabad", "lat": 22.9978, "lng": 72.6033},
    {"name": "Flipkart Hub - Vastrapur", "address": "Vastrapur, Ahmedabad", "lat": 23.0350, "lng": 72.5293},
    {"name": "Flipkart Hub - Ashram Road", "address": "Ashram Road, Ahmedabad", "lat": 23.0412, "lng": 72.5714},
]

DEMO_CAFES = [
    {"name": "Cafe Mocha", "lat": 23.0338, "lng": 72.5566},
    {"name": "Zen Cafe", "lat": 23.0372, "lng": 72.5510},
    {"name": "The Project Cafe", "lat": 23.0270, "lng": 72.5070},
    {"name": "Farzi Cafe", "lat": 23.0600, "lng": 72.5800},
]


def show_restaurant_location(request):
    address = request.GET.get('address', 'IIM Ahmedabad, Gujarat')
    lat, lng = get_coordinates(address)

    nearby_cafes = []
    if lat and lng:
        nearby_cafes = find_nearby_cafes(lat, lng, DEMO_CAFES)

    context = {
        'address': address,
        'lat': lat,
        'lng': lng,
        'api_key': settings.GOOGLE_MAPS_API_KEY,
        'nearby_cafes': nearby_cafes
    }
    return render(request, 'restaurant_location.html', context)


def search_by_distance(request):
    results = []
    user_address = request.GET.get('address', '')
    user_lat, user_lng = None, None

    if user_address:
        user_lat, user_lng = get_coordinates(user_address)
        if user_lat and user_lng:
            for pt in PICKUP_POINTS:
                dist = haversine_distance(user_lat, user_lng, pt['lat'], pt['lng'])
                item = pt.copy()
                item['distance'] = dist
                results.append(item)
            results.sort(key=lambda x: x['distance'])

    context = {
        'user_address': user_address,
        'user_lat': user_lat,
        'user_lng': user_lng,
        'results': results
    }
    return render(request, 'search_distance.html', context)