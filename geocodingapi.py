import requests
from config import API_KEY

BASE_URL = "https://api.openweathermap.org/geo/1.0/direct"



class GeocodingApi:
    @staticmethod
    def get_coordinates(city_name):
        params = {
            "q": city_name,
            "appid": API_KEY,
            "limit": 1
        }

        try:
            response = requests.get(
                BASE_URL,
                params=params,
                timeout=5
            )

            response.raise_for_status()

            coordinates = response.json()

            if not coordinates:
                print("City not found.")
                return None, None, None, None

            city = coordinates[0]
            country=city["country"]
            city_name = city["name"]

            lat = city["lat"]
            lon = city["lon"]

            return lat, lon,city_name,country

        except requests.exceptions.HTTPError:
            print("HTTP error.")
        except requests.exceptions.ConnectionError:
            print("Connection error.")
        except requests.exceptions.Timeout:
            print("Connection timed out.")
        except requests.exceptions.RequestException:
            print("Something went wrong.")

        return None, None, None, None