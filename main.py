import json
import requests

FILE_NAME = "favorite_cities.json"

WEATHER_URL = "https://api.open-meteo.com/v1/forecast"
GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"


def show_menu():
    print("""
===== Weather App =====

1. Check Weather
2. Check Favorite Cities
3. Add Favorite City
4. Remove Favorite City
5. Exit
""")


def get_city_name():
    return input("Enter city name: ").strip().lower()


def get_coordinates(city_name):
    params = {
        "name": city_name,
        "count": 1
    }

    try:
        response = requests.get(GEOCODING_URL, params=params, timeout=5)
        response.raise_for_status()

        data = response.json()

        if "results" not in data or len(data["results"]) == 0:
            print("City not found.")
            return None, None

        city = data["results"][0]

        return (
            city["latitude"],
            city["longitude"]
        )

    except requests.exceptions.HTTPError:
        print("HTTP Error.")
    except requests.exceptions.ConnectionError:
        print("Connection error.")
    except requests.exceptions.Timeout:
        print("Connection timed out.")
    except requests.exceptions.RequestException:
        print("Something went wrong.")

    return None, None


def get_weather(latitude, longitude):
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": "temperature_2m,relative_humidity_2m,wind_speed_10m"
    }

    try:
        response = requests.get(WEATHER_URL, params=params, timeout=5)
        response.raise_for_status()

        data = response.json()

        if "current" not in data:
            print("Unexpected API response.")
            return None

        return data["current"]

    except requests.exceptions.HTTPError:
        print("HTTP Error.")
    except requests.exceptions.ConnectionError:
        print("Connection error.")
    except requests.exceptions.Timeout:
        print("Connection timed out.")
    except requests.exceptions.RequestException:
        print("Something went wrong.")

    return None


def display_weather(city_name):
    latitude, longitude = get_coordinates(city_name)

    if latitude is None:
        return

    weather = get_weather(latitude, longitude)

    if weather is None:
        return

    print("\n==============================")
    print(f"City: {city_name.title()}")
    print("------------------------------")
    print(f"Temperature : {weather['temperature_2m']} °C")
    print(f"Humidity    : {weather['relative_humidity_2m']} %")
    print(f"Wind Speed  : {weather['wind_speed_10m']} km/h")
    print("==============================\n")


def load_data():
    try:
        with open(FILE_NAME, "r", encoding="utf-8") as file:
            return json.load(file)

    except FileNotFoundError:
        return []

    except json.JSONDecodeError:
        print("Invalid JSON file. Starting with an empty list.")
        return []


def save_data(favorite_cities):
    with open(FILE_NAME, "w", encoding="utf-8") as file:
        json.dump(
            favorite_cities,
            file,
            indent=4,
            ensure_ascii=False
        )


def add_favorite_city(favorite_cities):
    while True:

        city = get_city_name()

        if not city:
            print("City name cannot be empty.")
            continue

        duplicate = any(
            favorite["name"] == city
            for favorite in favorite_cities
        )

        if duplicate:
            print("City already exists.")
            continue

        favorite_cities.append({"name": city})

        save_data(favorite_cities)

        print("City added successfully!")
        return


def delete_favorite_city(favorite_cities):
    if not favorite_cities:
        print("No favorite cities found.")
        return

    for index, city in enumerate(favorite_cities, start=1):
        print(f"{index}. {city['name'].title()}")

    while True:

        try:
            choice = int(input("Select city number: "))

            if choice not in range(1, len(favorite_cities) + 1):
                print("Invalid option.")
                continue

            deleted_city = favorite_cities.pop(choice - 1)

            save_data(favorite_cities)

            print(f"{deleted_city['name'].title()} removed successfully!")
            return

        except ValueError:
            print("Please enter a valid number.")


def show_favorite_cities_weather(favorite_cities):
    if not favorite_cities:
        print("No favorite cities found.")
        return

    for city in favorite_cities:
        display_weather(city["name"])


def main():
    favorite_cities = load_data()

    while True:

        show_menu()

        try:
            choice = int(input("Select option (1-5): "))

            if choice not in range(1, 6):
                print("Invalid option.")
                continue

        except ValueError:
            print("Please enter a valid number.")
            continue

        if choice == 1:
            city = get_city_name()
            display_weather(city)

        elif choice == 2:
            show_favorite_cities_weather(favorite_cities)

        elif choice == 3:
            add_favorite_city(favorite_cities)

        elif choice == 4:
            delete_favorite_city(favorite_cities)

        elif choice == 5:
            print("Thank you for using Weather App!")
            break


if __name__ == "__main__":
    main()