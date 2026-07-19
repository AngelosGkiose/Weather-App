from weathersystem import WeatherSystem


def show_menu():
    print("""===== Weather Application =====

1. Current Weather
2. 5-Day Forecast
3. Air Quality
4. View Search History
5. Save Favorite City
6. View Weather Favorite Cities
7. Remove Favorite City
8. Exit""")


def main():
    system = WeatherSystem()

    while True:
        show_menu()

        try:
            user_choice = int(input("Enter your choice: ").strip())
        except ValueError:
            print("Please enter a number from 1 to 8.")
            continue

        if user_choice == 1:
            system.display_weather()
        elif user_choice == 2:
            system.display_forecast()
        elif user_choice == 3:
            system.display_air_quality()
        elif user_choice == 4:
            system.display_search_history()
        elif user_choice == 5:
            system.save_favourite_city()
        elif user_choice == 6:
            system.display_favorite_cities_weather()
        elif user_choice == 7:
            system.remove_fav_city()
        elif user_choice == 8:
            print("Exiting...")
            break
        else:
            print("Please enter a number from 1 to 8.")


if __name__ == "__main__":
    main()