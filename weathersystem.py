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
        print("===== Current Weather =====")
        print()
        print(weather)


    def display_forecast(self):
        city_name = input("Enter city name: ").strip()
        if not city_name:
            print("Please enter a city name.")
            return
        lat, lon = GeocodingApi.get_coordinates(city_name)
        if lat is None or lon is None:
            return
        forecast_list = WeatherApi.get_forecast(lat, lon)
        if not forecast_list:
            return
        print("===== 5-Day Forecast =====")
        print()
        for weather in forecast_list:
            print(f"Date: {weather.date}\n\n")
            print(weather)
            print("\n")
