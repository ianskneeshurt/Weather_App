import requests
import time
from http import HTTPStatus
from requests.exceptions import HTTPError

class NationalWeather:

    def get_grid(self, coordinates):
        """takes lat,lon coordinates, returns endpoint needed to get hourly forecast"""
        lat = coordinates.split(",")[0]
        lon = coordinates.split(",")[1]
        endpoint = f"https://api.weather.gov/points/{lat},{lon}"

        response = requests.get(url=endpoint)
        response.raise_for_status()
        data = response.json()["properties"]
        office = data["gridId"]
        grid_x = data["gridX"]
        grid_y = data["gridY"]
        api_endpoint_string = f"https://api.weather.gov/gridpoints/{office}/{grid_x},{grid_y}/forecast/hourly"
        return api_endpoint_string

    def get_weather(self, place_url):
        """takes nws request url, returns json weather data"""
        for n in range(5):
            try:
                response = requests.get(url=place_url)
                response.raise_for_status()
                data = response.json()
                return data
            except HTTPError as exc:
                if exc.response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR:
                    time.sleep(3)
                    continue
                raise

    def make_weather_dict(self, url_dict):
        """takes dict of nws request urls, returns new dictionary of json weather data for each place (weather_dict)"""
        weather_dict = {}
        for name, url in url_dict.items():
            weather_dict[name] = self.get_weather(url)

        return weather_dict

