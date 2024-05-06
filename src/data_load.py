import os
from dotenv import load_dotenv
import requests
from geopy.geocoders import Nominatim
from google.cloud import bigquery

# Load environment variables
load_dotenv(r"C:\Users\piotr\Downloads\Air_pollution\secrets\.env")
openweather_key_api = os.environ['OPENWEATHER_API_KEY']

# Initialize Google BigQuery client
client = bigquery.Client.from_service_account_json(r'C:\Users\piotr\Downloads\Air_pollution\secrets\openweather-421711-1472594dde96.json')

# Define the BigQuery table to send data to
table_id = "openweather-421711.air_pollution.pollution_1"

# Initialize geolocator
geolocator = Nominatim(user_agent='myapplication')

# Define cities
cities = ['Bydgoszcz', 'Gdańsk', 'Katowice', 'Kraków', 'Lublin', 
          'Poznań', 'Szczecin', 'Warszawa', 'Wrocław', 'Lublin']

# Base URL for OpenWeatherMap API
BASE_URL = "http://api.openweathermap.org/data/2.5/air_pollution?"

# Define schema for BigQuery table
schema = [
    bigquery.SchemaField("lat", "FLOAT"),
    bigquery.SchemaField("lon", "FLOAT"),
    bigquery.SchemaField("aqi", "INTEGER"),
    bigquery.SchemaField("co", "FLOAT"),
    bigquery.SchemaField("no", "FLOAT"),
    bigquery.SchemaField("no2", "FLOAT"),
    bigquery.SchemaField("o3", "FLOAT"),
    bigquery.SchemaField("so2", "FLOAT"),
    bigquery.SchemaField("pm2_5", "FLOAT"),
    bigquery.SchemaField("pm10", "FLOAT"),
    bigquery.SchemaField("nh3", "FLOAT"),
    bigquery.SchemaField("dt", "TIMESTAMP")
]

# Create BigQuery table if not exists
try:
    table = client.get_table(table_id)
except:
    table = bigquery.Table(table_id, schema=schema)
    table = client.create_table(table)

# Loop through cities and fetch data
for city in cities:
    location = geolocator.geocode(city)
    lat = location.raw['lat']
    lon = location.raw['lon']
    url = BASE_URL + "lat=" + lat + "&lon=" + lon + "&appid=" + openweather_key_api
    response = requests.get(url).json()
    
    # Extract data and load into BigQuery table
    for data in response['list']:
        row = {
            "lat": float(lat),
            "lon": float(lon),
            "aqi": data['main']['aqi'],
            "co": data['components']['co'],
            "no": data['components']['no'],
            "no2": data['components']['no2'],
            "o3": data['components']['o3'],
            "so2": data['components']['so2'],
            "pm2_5": data['components']['pm2_5'],
            "pm10": data['components']['pm10'],
            "nh3": data['components']['nh3'],
            "dt": data['dt']
        }
        errors = client.insert_rows_json(table, [row], row_ids=[None])  # Insert row into BigQuery table
        if errors:
            print(f"Errors occurred: {errors}")

print("Data loaded into BigQuery table.")
