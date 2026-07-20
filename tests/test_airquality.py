import requests
from unittest.mock import Mock, patch

from airquality import AirQuality
from airqualityapi import AirQualityApi


def test_get_air_quality_success():
    mock_response = Mock()
    mock_response.json.return_value = {
        "list": [
            {
                "main": {
                    "aqi": 2
                },
                "components": {
                    "pm2_5": 12.45,
                    "pm10": 20.30,
                    "co": 180.50,
                    "no2": 14.20,
                    "o3": 55.80
                }
            }
        ]
    }
    mock_response.raise_for_status.return_value = None


    with patch("airqualityapi.requests.get", return_value=mock_response):
        result = AirQualityApi.get_air_quality(
            37.9838,
            23.7275,
            "Athens",
            "GR"
        )


    assert isinstance(result, AirQuality)
    assert result.city == "Athens"
    assert result.country == "GR"
    assert result.aqi == 2
    assert result.quality == "Fair"
    assert result.pm2_5 == 12.45
    assert result.pm10 == 20.30
    assert result.co == 180.50
    assert result.no2 == 14.20
    assert result.o3 == 55.80


def test_get_air_quality_maps_all_aqi_levels():

    expected_levels = {
        1: "Good",
        2: "Fair",
        3: "Moderate",
        4: "Poor",
        5: "Very Poor"
    }

    for aqi, expected_quality in expected_levels.items():
        mock_response = Mock()
        mock_response.json.return_value = {
            "list": [
                {
                    "main": {
                        "aqi": aqi
                    },
                    "components": {
                        "pm2_5": 10.0,
                        "pm10": 20.0,
                        "co": 100.0,
                        "no2": 15.0,
                        "o3": 40.0
                    }
                }
            ]
        }
        mock_response.raise_for_status.return_value = None


        with patch(
            "airqualityapi.requests.get",
            return_value=mock_response
        ):
            result = AirQualityApi.get_air_quality(
                37.9838,
                23.7275,
                "Athens",
                "GR"
            )


        assert result.quality == expected_quality


@patch("airqualityapi.requests.get")
def test_get_air_quality_calls_api_correctly(mock_get):

    mock_response = Mock()
    mock_response.json.return_value = {
        "list": [
            {
                "main": {
                    "aqi": 1
                },
                "components": {
                    "pm2_5": 10.0,
                    "pm10": 20.0,
                    "co": 100.0,
                    "no2": 15.0,
                    "o3": 40.0
                }
            }
        ]
    }
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response


    AirQualityApi.get_air_quality(
        37.9838,
        23.7275,
        "Athens",
        "GR"
    )


    mock_get.assert_called_once()

    called_url = mock_get.call_args.args[0]
    called_params = mock_get.call_args.kwargs["params"]
    called_timeout = mock_get.call_args.kwargs["timeout"]

    assert called_url == (
        "https://api.openweathermap.org/data/2.5/air_pollution"
    )
    assert called_params["lat"] == 37.9838
    assert called_params["lon"] == 23.7275
    assert "appid" in called_params
    assert called_timeout == 5


def test_get_air_quality_http_error(capsys):

    mock_response = Mock()
    mock_response.raise_for_status.side_effect = (
        requests.exceptions.HTTPError
    )


    with patch("airqualityapi.requests.get", return_value=mock_response):
        result = AirQualityApi.get_air_quality(
            37.9838,
            23.7275,
            "Athens",
            "GR"
        )

    captured = capsys.readouterr()


    assert result is None
    assert "HTTP error." in captured.out


def test_get_air_quality_connection_error(capsys):

    with patch(
        "airqualityapi.requests.get",
        side_effect=requests.exceptions.ConnectionError
    ):
        result = AirQualityApi.get_air_quality(
            37.9838,
            23.7275,
            "Athens",
            "GR"
        )

    captured = capsys.readouterr()


    assert result is None
    assert "Connection error." in captured.out


def test_get_air_quality_timeout(capsys):

    with patch(
        "airqualityapi.requests.get",
        side_effect=requests.exceptions.Timeout
    ):
        result = AirQualityApi.get_air_quality(
            37.9838,
            23.7275,
            "Athens",
            "GR"
        )

    captured = capsys.readouterr()

    assert result is None
    assert "Connection timed out." in captured.out


def test_get_air_quality_request_exception(capsys):

    with patch(
        "airqualityapi.requests.get",
        side_effect=requests.exceptions.RequestException
    ):
        result = AirQualityApi.get_air_quality(
            37.9838,
            23.7275,
            "Athens",
            "GR"
        )

    captured = capsys.readouterr()

   
    assert result is None
    assert "Something went wrong." in captured.out