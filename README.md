#  Weather App

A command-line Weather App built with Python that retrieves real-time weather data using the Open-Meteo API.

The application allows users to search for weather information by city, save favorite cities, and quickly view the weather for all saved locations.

---

## Features

-  Search weather by city
-  View current temperature
-  View humidity
-  View wind speed
-  Add favorite cities
-  Remove favorite cities
-  Save favorite cities in a JSON file
-  Error handling for invalid cities, network issues, and invalid JSON files

---

## Technologies Used

- Python 3
- Requests
- JSON
- Open-Meteo API

---

## Project Structure

```
Weather-App/
│
├── weather_app.py
├── favorite_cities.json
├── requirements.txt
├── README.md
└── .gitignore
```

---

## Installation

Clone the repository:

```bash
git clone https://github.com/yourusername/weather-app.git
```

Move into the project folder:

```bash
cd weather-app
```

Install the required package:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
python weather_app.py
```

---

## Example

```
===== Weather App =====

1. Check Weather
2. Check Favorite Cities
3. Add Favorite City
4. Remove Favorite City
5. Exit
```

Example output:

```
==============================
City: Athens
------------------------------
Temperature : 31 °C
Humidity    : 46 %
Wind Speed  : 5.8 km/h
==============================
```

---

## What I Learned

This project helped me practice:

- Working with REST APIs
- Sending HTTP requests
- Parsing JSON responses
- Reading and writing JSON files
- Error handling with try/except
- Organizing Python code into reusable functions
- Building a complete command-line application

---

## Future Improvements

- 5-day weather forecast
- Weather condition descriptions
- Weather icons
- Search history
- Unit conversion (°C / °F)
- Better terminal formatting

---

## License

This project is open source and available under the MIT License.
