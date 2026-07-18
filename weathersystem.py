from geocodingapi import GeocodingApi
from weatherapi import WeatherApi


class WeatherSystem:
    def display_weather(self):
        city_name = input("Enter city name: ").strip()

        if not city_name:
            print("Please enter a city name.")
            return

        lat, lon = GeocodingApi.get_coordinates(city_name)

        if lat is None or lon is None:
            return

        weather = WeatherApi.get_weather(lat, lon)

        if weather is None:
            return

        print()
        print(weather)