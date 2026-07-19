from database import Database
from airqualityapi import AirQualityApi
from favoritecity import FavoriteCity
from geocodingapi import GeocodingApi
from weatherapi import WeatherApi


class WeatherSystem:

    def __init__(self):
        self.database=Database()

    def display_weather(self):
        city_name = input("Enter city name: ").strip()

        if not city_name:
            print("Please enter a city name.")
            return

        lat,lon,city_name,country = GeocodingApi.get_coordinates(city_name)

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
        lat, lon,city_name,country = GeocodingApi.get_coordinates(city_name)
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

    def display_air_quality(self):
        city_name = input("Enter city name: ").strip()
        if not city_name:
            print("Please enter a city name.")
            return
        lat, lon,city_name,country = GeocodingApi.get_coordinates(city_name)
        if lat is None or lon is None:
            return
        air_quality = AirQualityApi.get_air_quality(lat, lon, city_name, country)
        if air_quality is None:
            return
        print("===== Air Quality =====")
        print()
        print(air_quality)

    def save_favourite_city(self):
        city_name = input("Enter city name: ").strip()
        if not city_name:
            print("Please enter a city name.")
            return
        lat, lon,city_name,country = GeocodingApi.get_coordinates(city_name)
        if lat is None or lon is None:
            return
        favorite_city=FavoriteCity(city_name=city_name, country=country, latitude=lat, longitude=lon)
        completed=self.database.add_favorite_city(favorite_city)
        if completed:
            print(f"{city_name},{country} was  added to your favorite cities.")
        else:
            print(f"{city_name},{country} is already in your favorite cities.")

    def display_favorite_cities_weather(self):
        favorite_cities =self.database.get_favorite_city()
        if not favorite_cities :
            print("No favorite cities were found.")
            return
        for fav_city in favorite_cities :
            weather = WeatherApi.get_weather(fav_city.latitude,fav_city.longitude)
            if weather is None:
                print(
                    f"Could not retrieve weather for "
                    f"{fav_city.city_name}, {fav_city.country}."
                )
                print()
                continue
            print("===== Current Weather =====")
            print()
            print(weather)

    def remove_fav_city(self):
        favorite_city = self.database.get_favorite_city()
        if not favorite_city:
            print("No favorite cities were found.")
            return
        for fav_city in favorite_city :
            print(fav_city)
        try:
            city_id=int(input("Enter city ID to remove: "))
            if city_id<=0 :
                print("Please enter a valid city ID.")
        except ValueError:
            print("Please enter a numeric city ID.")
            return
        city=self.database.get_favorite_city_by_id(city_id)
        if city is None:
            print("No favorite cities with this id  were found.")
            return
        completed=self.database.delete_favorite_city(city)
        if completed:
            f"{city.city_name}, {city.country} was removed "
            f"from your favorite cities."
        else:
            print("The favorite city could not be removed.")



