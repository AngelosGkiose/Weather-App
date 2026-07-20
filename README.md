# Weather App

A command-line Weather Application built with Python that retrieves real-time weather, 5-day forecasts, and air quality information using the OpenWeather API.

## Features

- Current weather by city
- 5-day weather forecast
- Air quality information
- Save favorite cities
- View weather for favorite cities
- Search history
- SQLite database for data persistence
- Input validation and error handling
- Comprehensive unit tests with pytest

## Technologies

- Python 3
- SQLite
- Requests
- OpenWeather API
- Pytest
- unittest.mock
- python-dotenv

## Project Structure

```
Weather-App/
│
├── tests/
├── airquality.py
├── airqualityapi.py
├── database.py
├── favoritecity.py
├── geocodingapi.py
├── searchhistory.py
├── weather.py
├── weatherapi.py
├── weathersystem.py
├── main.py
├── requirements.txt
├── .env.example
└── README.md
```

## Installation

Clone the repository:

```bash
git clone https://github.com/your-username/Weather-App.git
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file:

```env
OPENWEATHER_API_KEY=your_api_key
```

## Usage

Run the application:

```bash
python main.py
```

## Running Tests

Run all tests:

```bash
python -m pytest
```

Run tests with coverage:

```bash
python -m pytest --cov=. --cov-report=term-missing
```

## Test Coverage

- 65 unit tests
- 95% code coverage
- API requests tested using mocks
- SQLite tested using an in-memory database
- Business logic fully tested

## What I Learned

During this project I practiced:

- Object-Oriented Programming (OOP)
- REST API integration
- HTTP requests with Requests
- SQLite database design
- Environment variables with dotenv
- Unit testing with pytest
- Mocking external APIs
- Git and GitHub workflow

