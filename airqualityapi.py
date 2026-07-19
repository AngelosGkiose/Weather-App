import requests

from airquality import AirQuality
from config import API_KEY


BASE_URL = "https://api.openweathermap.org/data/2.5/air_pollution"


class AirQualityApi:
    @staticmethod
    def get_air_quality(lat, lon, city_name, country):
        params = {
            "lat": lat,
            "lon": lon,
            "appid": API_KEY
        }
        aqi_levels = {
            1: "Good",
            2: "Fair",
            3: "Moderate",
            4: "Poor",
            5: "Very Poor"
        }
        try:
            response = requests.get(
                BASE_URL,
                params=params,
                timeout=5
            )
            response.raise_for_status()
            airquality_json = response.json()
            air_data = airquality_json["list"][0]
            main_data = air_data["main"]
            components = air_data["components"]
            aqi = main_data["aqi"]
            return AirQuality(
                city=city_name,
                country=country,
                aqi=aqi,
                quality=aqi_levels[aqi],
                pm2_5=components["pm2_5"],
                pm10=components["pm10"],
                co=components["co"],
                no2=components["no2"],
                o3=components["o3"]
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