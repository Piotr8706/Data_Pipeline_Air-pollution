import os
from dotenv import load_dotenv
load_dotenv('secrets/.env')
openweather_key_api = os.environ['OPENWEATHER_API_KEY']