import requests
from config import Config

def get_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={Config.OPENWEATHER_API_KEY}&units=metric"
    try:
        response = requests.get(url)
        data = response.json()
        return data['main']['temp']
    except:
        return 25  # Default temperature
