import requests

from weather import Weather
from config import API_KEY

BASE_URL = "https://api.openweathermap.org/data/2.5/weather"



class WeatherApi:
    @staticmethod
    def get_weather(lat, lon):
        params = {
            "lat": lat,
            "lon": lon,
            "appid": API_KEY,
            "units": "metric",
            "lang": "en"
        }

        try:
            response = requests.get(
                BASE_URL,
                params=params,
                timeout=5
            )

            response.raise_for_status()

            weather_json = response.json()

            weather_data = weather_json["weather"][0]
            main_data = weather_json["main"]
            wind_data = weather_json["wind"]
            system_data = weather_json["sys"]

            return Weather(
                city=weather_json["name"],
                country=system_data["country"],
                temperature=main_data["temp"],
                feels_like=main_data["feels_like"],
                condition=weather_data["main"],
                description=weather_data["description"],
                humidity=main_data["humidity"],
                pressure=main_data["pressure"],
                wind_speed=wind_data["speed"]
            )

        except requests.exceptions.HTTPError:
            print("HTTP error.")
        except requests.exceptions.ConnectionError:
            print("Connection error.")
        except requests.exceptions.Timeout:
            print("Connection timed out.")
        except requests.exceptions.RequestException:
            print("Something went wrong.")

        return None