import json
from geopy.geocoders import Nominatim

def get_and_load_coordinates(cities, api_key, ti=None):
    geolocator = Nominatim(user_agent='myapplication')
    city_coordinates = {}

    for city in cities:
        location = geolocator.geocode(city)
        lat = location.latitude
        lon = location.longitude
        city_coordinates[city] = {"lat": lat, "lon": lon}

    cities_coordinates = json.dumps(city_coordinates)
    if ti is not None:
        ti.xcom_push(key='cities_coordinates', value=cities_coordinates)