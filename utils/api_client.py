import requests

class WeatherApiClient:
    BASE_URL = "http://api.weatherapi.com/v1"

    def __init__(self, api_key):
        self.api_key = api_key

    def get_current_weather(self, location):
        url = f"{self.BASE_URL}/current.json?key={self.api_key}&q={location}"
        response = requests.get(url)
        return response

    def get_forecast(self, location, days):
        url = f"{self.BASE_URL}/forecast.json?key={self.api_key}&q={location}&days={days}"
        response = requests.get(url)
        return response

    def post_example(self, endpoint, payload):
        url = f"{self.BASE_URL}/{endpoint}"
        response = requests.post(url, json=payload)
        return response
