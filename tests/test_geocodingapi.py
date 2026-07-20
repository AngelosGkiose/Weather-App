import requests
from unittest.mock import Mock, patch

from geocodingapi import GeocodingApi


def test_get_coordinates_success():
    mock_response = Mock()
    mock_response.json.return_value = [
        {
            "name": "Athens",
            "country": "GR",
            "lat": 37.9838,
            "lon": 23.7275
        }
    ]
    mock_response.raise_for_status.return_value = None

    with patch("geocodingapi.requests.get", return_value=mock_response):
        result = GeocodingApi.get_coordinates("Athens")

    assert result == (37.9838, 23.7275, "Athens", "GR")


def test_get_coordinates_city_not_found(capsys):
    mock_response = Mock()
    mock_response.json.return_value = []
    mock_response.raise_for_status.return_value = None

    with patch("geocodingapi.requests.get", return_value=mock_response):
        result = GeocodingApi.get_coordinates("UnknownCity")

    captured = capsys.readouterr()

    assert result == (None, None, None, None)
    assert "City not found." in captured.out


def test_get_coordinates_http_error(capsys):
    mock_response = Mock()
    mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError

    with patch("geocodingapi.requests.get", return_value=mock_response):
        result = GeocodingApi.get_coordinates("Athens")

    captured = capsys.readouterr()

    assert result == (None, None, None, None)
    assert "HTTP error." in captured.out


def test_get_coordinates_timeout(capsys):
    with patch(
        "geocodingapi.requests.get",
        side_effect=requests.exceptions.Timeout
    ):
        result = GeocodingApi.get_coordinates("Athens")

    captured = capsys.readouterr()

    assert result == (None, None, None, None)
    assert "Connection timed out." in captured.out


def test_get_coordinates_connection_error(capsys):
    with patch(
        "geocodingapi.requests.get",
        side_effect=requests.exceptions.ConnectionError
    ):
        result = GeocodingApi.get_coordinates("Athens")

    captured = capsys.readouterr()

    assert result == (None, None, None, None)
    assert "Connection error." in captured.out


@patch("geocodingapi.requests.get")
def test_get_coordinates_calls_api_correctly(mock_get):
    mock_response = Mock()
    mock_response.json.return_value = [
        {
            "name": "Athens",
            "country": "GR",
            "lat": 37.9838,
            "lon": 23.7275
        }
    ]
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    GeocodingApi.get_coordinates("Athens")

    mock_get.assert_called_once()

    called_url = mock_get.call_args.args[0]
    called_params = mock_get.call_args.kwargs["params"]
    called_timeout = mock_get.call_args.kwargs["timeout"]

    assert called_url == "https://api.openweathermap.org/geo/1.0/direct"
    assert called_params["q"] == "Athens"
    assert called_params["limit"] == 1
    assert "appid" in called_params
    assert called_timeout == 5