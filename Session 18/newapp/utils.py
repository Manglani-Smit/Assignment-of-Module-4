import math
import requests


def get_coordinates(address):
    url = "https://nominatim.openstreetmap.org/search"
    headers = {"User-Agent": "DjangoTopsAssignmentApp/1.0"}
    params = {"q": address, "format": "json", "limit": 1}

    try:
        response = requests.get(url, params=params, headers=headers, timeout=5).json()
        if response:
            return float(response[0]["lat"]), float(response[0]["lon"])
    except Exception:
        pass
    return None, None


def haversine_distance(lat1, lon1, lat2, lon2):
    R = 6371.0
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)

    a = (math.sin(dlat / 2) ** 2 +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
         math.sin(dlon / 2) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return round(R * c, 2)


def find_nearby_cafes(user_lat, user_lng, cafes):
    nearby = []
    for cafe in cafes:
        dist = haversine_distance(user_lat, user_lng, cafe['lat'], cafe['lng'])
        if dist <= 3.0:
            cafe_data = cafe.copy()
            cafe_data['distance'] = dist
            nearby.append(cafe_data)
    return nearby