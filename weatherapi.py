import requests

from weather import Weather
from config import API_KEY

WEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"
FORECAST_URL = "https://api.openweathermap.org/data/2.5/forecast"



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
                WEATHER_URL,
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

    @staticmethod
    def get_forecast(lat, lon):
        params = {
            "lat": lat,
            "lon": lon,
            "appid": API_KEY,
            "units": "metric",
            "cnt": 40
        }

        try:
            response = requests.get(
                FORECAST_URL,
                params=params,
                timeout=5
            )

            response.raise_for_status()

            forecast_json = response.json()
            city = forecast_json["city"]

            forecast_5_days = []

            for forecast in forecast_json["list"]:

                date_time = forecast["dt_txt"]
                date, time = date_time.split(" ")

                if time != "12:00:00":
                    continue

                main_data = forecast["main"]
                wind_data = forecast["wind"]
                weather_data = forecast["weather"][0]

                weather = Weather(
                    city=city["name"],
                    country=city["country"],
                    temperature=main_data["temp"],
                    feels_like=main_data["feels_like"],
                    condition=weather_data["main"],
                    description=weather_data["description"],
                    humidity=main_data["humidity"],
                    pressure=main_data["pressure"],
                    wind_speed=wind_data["speed"],
                    date=date
                )

                forecast_5_days.append(weather)

                if len(forecast_5_days) == 5:
                    break

            return forecast_5_days

        except requests.exceptions.HTTPError:
            print("HTTP error.")
        except requests.exceptions.ConnectionError:
            print("Connection error.")
        except requests.exceptions.Timeout:
            print("Connection timed out.")
        except requests.exceptions.RequestException:
            print("Something went wrong.")

        return None



