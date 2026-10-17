import math
import requests


# Q1: Geocoding Function (Free, No API Key needed)
def get_lat_lng(address):
    url = "https://nominatim.openstreetmap.org/search"
    headers = {"User-Agent": "DjangoTopsTester/1.0"}
    params = {"q": address, "format": "json", "limit": 1}

    res = requests.get(url, params=params, headers=headers).json()
    if res:
        return float(res[0]["lat"]), float(res[0]["lon"])
    return None, None


# Q3: Haversine Formula (Manual Calculation)
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
            item = cafe.copy()
            item['distance'] = dist
            nearby.append(item)
    return nearby


# === EXECUTION TEST ===
if __name__ == "__main__":
    print("----- Running Q1 Test: Geocoding -----")
    address = "IIM Ahmedabad, Gujarat"
    lat, lng = get_lat_lng(address)
    print(f"Target Address : {address}")
    print(f"Latitude       : {lat}")
    print(f"Longitude      : {lng}")
    print("---------------------------------------")

    print("\n----- Running Q3 Test: Nearby Cafes (<= 3 KM) -----")
    sample_cafes = [
        {"name": "Zen Cafe", "lat": 23.0372, "lng": 72.5510},
        {"name": "Cafe Mocha", "lat": 23.0338, "lng": 72.5566},
        {"name": "Remote Highway Cafe", "lat": 23.1500, "lng": 72.6500}
    ]

    if lat and lng:
        results = find_nearby_cafes(lat, lng, sample_cafes)
        for cafe in results:
            print(f"- {cafe['name']}: {cafe['distance']} km away")
    print("--------------------------------------------------")