import requests
from unittest.mock import Mock, patch

from weather import Weather
from weatherapi import WeatherApi


def test_get_weather_success():
    mock_response = Mock()
    mock_response.json.return_value = {
        "name": "Athens",
        "sys": {
            "country": "GR"
        },
        "weather": [
            {
                "main": "Clear",
                "description": "clear sky"
            }
        ],
        "main": {
            "temp": 30.5,
            "feels_like": 32.0,
            "humidity": 40,
            "pressure": 1013
        },
        "wind": {
            "speed": 3.5
        }
    }
    mock_response.raise_for_status.return_value = None


    with patch("weatherapi.requests.get", return_value=mock_response):
        result = WeatherApi.get_weather(37.9838, 23.7275)


    assert isinstance(result, Weather)
    assert result.city == "Athens"
    assert result.country == "GR"
    assert result.temperature == 30.5
    assert result.feels_like == 32.0
    assert result.condition == "Clear"
    assert result.description == "clear sky"
    assert result.humidity == 40
    assert result.pressure == 1013
    assert result.wind_speed == 3.5
    assert result.date is None


@patch("weatherapi.requests.get")
def test_get_weather_calls_api_correctly(mock_get):

    mock_response = Mock()
    mock_response.json.return_value = {
        "name": "Athens",
        "sys": {
            "country": "GR"
        },
        "weather": [
            {
                "main": "Clear",
                "description": "clear sky"
            }
        ],
        "main": {
            "temp": 30.5,
            "feels_like": 32.0,
            "humidity": 40,
            "pressure": 1013
        },
        "wind": {
            "speed": 3.5
        }
    }
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response


    WeatherApi.get_weather(37.9838, 23.7275)


    mock_get.assert_called_once()

    called_url = mock_get.call_args.args[0]
    called_params = mock_get.call_args.kwargs["params"]
    called_timeout = mock_get.call_args.kwargs["timeout"]

    assert called_url == (
        "https://api.openweathermap.org/data/2.5/weather"
    )
    assert called_params["lat"] == 37.9838
    assert called_params["lon"] == 23.7275
    assert called_params["units"] == "metric"
    assert called_params["lang"] == "en"
    assert "appid" in called_params
    assert called_timeout == 5


def test_get_weather_http_error(capsys):

    mock_response = Mock()
    mock_response.raise_for_status.side_effect = (
        requests.exceptions.HTTPError
    )


    with patch("weatherapi.requests.get", return_value=mock_response):
        result = WeatherApi.get_weather(37.9838, 23.7275)

    captured = capsys.readouterr()


    assert result is None
    assert "HTTP error." in captured.out


def test_get_weather_connection_error(capsys):

    with patch(
        "weatherapi.requests.get",
        side_effect=requests.exceptions.ConnectionError
    ):
        result = WeatherApi.get_weather(37.9838, 23.7275)

    captured = capsys.readouterr()


    assert result is None
    assert "Connection error." in captured.out


def test_get_weather_timeout(capsys):

    with patch(
        "weatherapi.requests.get",
        side_effect=requests.exceptions.Timeout
    ):
        result = WeatherApi.get_weather(37.9838, 23.7275)

    captured = capsys.readouterr()


    assert result is None
    assert "Connection timed out." in captured.out


def test_get_weather_request_exception(capsys):

    with patch(
        "weatherapi.requests.get",
        side_effect=requests.exceptions.RequestException
    ):
        result = WeatherApi.get_weather(37.9838, 23.7275)

    captured = capsys.readouterr()


    assert result is None
    assert "Something went wrong." in captured.out


def test_get_forecast_success():

    mock_response = Mock()
    mock_response.json.return_value = {
        "city": {
            "name": "Athens",
            "country": "GR"
        },
        "list": [
            {
                "dt_txt": "2026-07-21 09:00:00",
                "main": {
                    "temp": 28.0,
                    "feels_like": 29.0,
                    "humidity": 45,
                    "pressure": 1012
                },
                "wind": {
                    "speed": 2.5
                },
                "weather": [
                    {
                        "main": "Clouds",
                        "description": "few clouds"
                    }
                ]
            },
            {
                "dt_txt": "2026-07-21 12:00:00",
                "main": {
                    "temp": 30.0,
                    "feels_like": 31.0,
                    "humidity": 40,
                    "pressure": 1013
                },
                "wind": {
                    "speed": 3.0
                },
                "weather": [
                    {
                        "main": "Clear",
                        "description": "clear sky"
                    }
                ]
            },
            {
                "dt_txt": "2026-07-22 12:00:00",
                "main": {
                    "temp": 31.0,
                    "feels_like": 32.0,
                    "humidity": 38,
                    "pressure": 1011
                },
                "wind": {
                    "speed": 3.5
                },
                "weather": [
                    {
                        "main": "Clear",
                        "description": "clear sky"
                    }
                ]
            }
        ]
    }
    mock_response.raise_for_status.return_value = None


    with patch("weatherapi.requests.get", return_value=mock_response):
        result = WeatherApi.get_forecast(37.9838, 23.7275)


    assert len(result) == 2

    first_forecast = result[0]

    assert isinstance(first_forecast, Weather)
    assert first_forecast.city == "Athens"
    assert first_forecast.country == "GR"
    assert first_forecast.temperature == 30.0
    assert first_forecast.feels_like == 31.0
    assert first_forecast.condition == "Clear"
    assert first_forecast.description == "clear sky"
    assert first_forecast.humidity == 40
    assert first_forecast.pressure == 1013
    assert first_forecast.wind_speed == 3.0
    assert first_forecast.date == "2026-07-21"

    second_forecast = result[1]

    assert second_forecast.temperature == 31.0
    assert second_forecast.date == "2026-07-22"


def test_get_forecast_returns_maximum_five_days():

    forecast_list = []

    for day in range(1, 7):
        forecast_list.append(
            {
                "dt_txt": f"2026-08-{day:02d} 12:00:00",
                "main": {
                    "temp": 30.0 + day,
                    "feels_like": 31.0 + day,
                    "humidity": 40,
                    "pressure": 1013
                },
                "wind": {
                    "speed": 3.0
                },
                "weather": [
                    {
                        "main": "Clear",
                        "description": "clear sky"
                    }
                ]
            }
        )

    mock_response = Mock()
    mock_response.json.return_value = {
        "city": {
            "name": "Athens",
            "country": "GR"
        },
        "list": forecast_list
    }
    mock_response.raise_for_status.return_value = None


    with patch("weatherapi.requests.get", return_value=mock_response):
        result = WeatherApi.get_forecast(37.9838, 23.7275)


    assert len(result) == 5
    assert result[0].date == "2026-08-01"
    assert result[4].date == "2026-08-05"


def test_get_forecast_returns_empty_list_without_midday_forecasts():

    mock_response = Mock()
    mock_response.json.return_value = {
        "city": {
            "name": "Athens",
            "country": "GR"
        },
        "list": [
            {
                "dt_txt": "2026-07-21 09:00:00",
                "main": {
                    "temp": 28.0,
                    "feels_like": 29.0,
                    "humidity": 45,
                    "pressure": 1012
                },
                "wind": {
                    "speed": 2.5
                },
                "weather": [
                    {
                        "main": "Clouds",
                        "description": "few clouds"
                    }
                ]
            }
        ]
    }
    mock_response.raise_for_status.return_value = None


    with patch("weatherapi.requests.get", return_value=mock_response):
        result = WeatherApi.get_forecast(37.9838, 23.7275)


    assert result == []


@patch("weatherapi.requests.get")
def test_get_forecast_calls_api_correctly(mock_get):

    mock_response = Mock()
    mock_response.json.return_value = {
        "city": {
            "name": "Athens",
            "country": "GR"
        },
        "list": []
    }
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response


    WeatherApi.get_forecast(37.9838, 23.7275)


    mock_get.assert_called_once()

    called_url = mock_get.call_args.args[0]
    called_params = mock_get.call_args.kwargs["params"]
    called_timeout = mock_get.call_args.kwargs["timeout"]

    assert called_url == (
        "https://api.openweathermap.org/data/2.5/forecast"
    )
    assert called_params["lat"] == 37.9838
    assert called_params["lon"] == 23.7275
    assert called_params["units"] == "metric"
    assert called_params["cnt"] == 40
    assert "appid" in called_params
    assert called_timeout == 5


def test_get_forecast_http_error(capsys):
    # Arrange
    mock_response = Mock()
    mock_response.raise_for_status.side_effect = (
        requests.exceptions.HTTPError
    )


    with patch("weatherapi.requests.get", return_value=mock_response):
        result = WeatherApi.get_forecast(37.9838, 23.7275)

    captured = capsys.readouterr()


    assert result is None
    assert "HTTP error." in captured.out


def test_get_forecast_connection_error(capsys):

    with patch(
        "weatherapi.requests.get",
        side_effect=requests.exceptions.ConnectionError
    ):
        result = WeatherApi.get_forecast(37.9838, 23.7275)

    captured = capsys.readouterr()


    assert result is None
    assert "Connection error." in captured.out


def test_get_forecast_timeout(capsys):

    with patch(
        "weatherapi.requests.get",
        side_effect=requests.exceptions.Timeout
    ):
        result = WeatherApi.get_forecast(37.9838, 23.7275)

    captured = capsys.readouterr()


    assert result is None
    assert "Connection timed out." in captured.out


def test_get_forecast_request_exception(capsys):

    with patch(
        "weatherapi.requests.get",
        side_effect=requests.exceptions.RequestException
    ):
        result = WeatherApi.get_forecast(37.9838, 23.7275)

    captured = capsys.readouterr()

  
    assert result is None
    assert "Something went wrong." in captured.out