from weathersystem import WeatherSystem


def show_menu():
    print("""===== Weather Application =====

1. Current Weather
2. 5-Day Forecast
3. Exit""")


def main():
    system = WeatherSystem()

    while True:
        show_menu()

        try:
            user_choice = int(input("Enter your choice: ").strip())
        except ValueError:
            print("Please enter a number from 1 to 3.")
            continue

        if user_choice == 1:
            system.display_weather()
        elif user_choice == 2:
            pass
        elif user_choice == 3:
            print("Exiting...")
            break
        else:
            print("Please enter a number from 1 to 3.")


if __name__ == "__main__":
    main()