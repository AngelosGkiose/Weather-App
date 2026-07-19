# Weather Application

A command-line Weather Application built with Python that uses the OpenWeather API to provide current weather, 5-day forecasts, and air quality information. The application also stores search history and favorite cities using SQLite.

## Features

- Current Weather
- 5-Day Weather Forecast
- Air Quality Information
- Search History
- Save Favorite Cities
- View Weather for Favorite Cities
- Remove Favorite Cities
- Input validation with cancel option

## Technologies

- Python
- SQLite
- Requests
- OpenWeather API
- python-dotenv

## Project Structure

```
weather_app/
│── main.py
│── weathersystem.py
│── weather.py
│── weatherapi.py
│── airquality.py
│── airqualityapi.py
│── favoritecity.py
│── searchhistory.py
│── geocodingapi.py
│── database.py
│── config.py
│── .env
```

## Installation

1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/weather-application.git
cd weather-application
```

2. Install the required package

```bash
pip install requests python-dotenv
```

3. Create a `.env` file in the project root

```env
OPENWEATHER_API_KEY=your_api_key_here
```

4. Run the application

```bash
python main.py
```

## Menu

```
===== Weather Application =====

1. Current Weather
2. 5-Day Forecast
3. Air Quality
4. View Search History
5. Save Favorite City
6. View Weather Favorite Cities
7. Remove Favorite City
8. Exit
```

## What I Practiced

- Object-Oriented Programming (OOP)
- SQLite database design
- API integration with Requests
- JSON data handling
- Error handling and input validation
- Code refactoring using helper methods
- Clean project structure

## Future Improvements

- Weather icons
- Search history filtering
- Favorite city updates
- Unit tests


