import os
from dotenv import load_dotenv

# load .env
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

# Weather
WEATHER_API_KEY = os.getenv("WEATHER_API") # API
WEATHER_API_URL = "http://api.openweathermap.org/data/2.5/weather" # Parameters
# Currency
CURRENCY_API_URL = "https://api.currencyfreaks.com/latest"
