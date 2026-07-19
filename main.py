from weathersystem import WeatherSystem


def show_menu():
    print("""===== Weather Application =====

1. Current Weather
2. 5-Day Forecast
3. Air Quality
3. View Search History
4. Save Favorite City
5. View Weather Favorite Cities
6. Remove Favorite City
7. Exit""")


def main():
    system = WeatherSystem()

    while True:
        show_menu()

        try:
            user_choice = int(input("Enter your choice: ").strip())
        except ValueError:
            print("Please enter a number from 1 to 5.")
            continue

        if user_choice == 1:
            system.display_weather()
        elif user_choice == 2:
            system.display_forecast()
        elif user_choice == 3:
            system.display_air_quality()
        elif user_choice == 4:
            system.save_favourite_city()
        elif user_choice == 5:
            system.display_favorite_cities_weather()
        elif user_choice == 6:
            system.remove_fav_city()
        elif user_choice == 7:
            print("Exiting...")
            break
        else:
            print("Please enter a number from 1 to 5.")


if __name__ == "__main__":
    main()