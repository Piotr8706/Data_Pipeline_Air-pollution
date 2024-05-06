import os
from dotenv import load_dotenv
import requests
from geopy.geocoders import Nominatim
import json

geolocator = Nominatim(user_agent='myapplication')
cities = ['Bydgoszcz', 'Gdańsk', 'Katowice', 'Kraków', 'Lublin', 
          'Poznań', 'Szczecin', 'Warszawa','Wrocław', 'Lublin']

load_dotenv(r"C:\Users\piotr\Downloads\Air_pollution\secrets\.env")
openweather_key_api = os.environ['OPENWEATHER_API_KEY']
BASE_URL = "http://api.openweathermap.org/data/2.5/air_pollution?"

# creating json for cities
for city in cities:
    location = geolocator.geocode(city)
    lat = location.raw['lat']
    lon = location.raw['lon']
    url = BASE_URL + "lat=" + lat + "&lon=" + lon + "&appid=" + openweather_key_api
    response = requests.get(url).json()
    with open(f"{city}_{response['list'][0]['dt']}.json", 'w', encoding='utf-8') as f:
        json.dump(response, f, ensure_ascii=False, indent=4)
