from unittest.mock import Mock, patch

import pytest

from airquality import AirQuality
from favoritecity import FavoriteCity
from weather import Weather
from weathersystem import WeatherSystem


@pytest.fixture
def weather_system():
    """
    Δημιουργεί WeatherSystem χωρίς να ανοίγει
    την πραγματική SQLite database.
    """
    system = WeatherSystem.__new__(WeatherSystem)
    system.database = Mock()

    return system


@pytest.fixture
def sample_weather():
    return Weather(
        city="Athens",
        country="GR",
        temperature=30.5,
        feels_like=32.0,
        condition="Clear",
        description="clear sky",
        humidity=40,
        pressure=1013,
        wind_speed=3.5
    )


@pytest.fixture
def sample_air_quality():
    return AirQuality(
        city="Athens",
        country="GR",
        aqi=2,
        quality="Fair",
        pm2_5=12.45,
        pm10=20.30,
        co=180.50,
        no2=14.20,
        o3=55.80
    )


def test_get_city_name_from_user_returns_city(monkeypatch):
    # Arrange
    monkeypatch.setattr("builtins.input", lambda _: "  Athens  ")

    # Act
    result = WeatherSystem.get_city_name_from_user()

    # Assert
    assert result == "Athens"


def test_get_city_name_from_user_cancel(monkeypatch, capsys):
    # Arrange
    monkeypatch.setattr("builtins.input", lambda _: "0")

    # Act
    result = WeatherSystem.get_city_name_from_user()

    captured = capsys.readouterr()

    # Assert
    assert result is None
    assert "Operation cancelled." in captured.out


def test_get_city_name_from_user_repeats_after_empty_input(
    monkeypatch,
    capsys
):
    # Arrange
    user_inputs = iter(["", "   ", "Athens"])
    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(user_inputs)
    )

    # Act
    result = WeatherSystem.get_city_name_from_user()

    captured = capsys.readouterr()

    # Assert
    assert result == "Athens"

    assert captured.out.count(
        "Please enter a city name."
    ) == 2


def test_display_weather_success(
    weather_system,
    sample_weather,
    capsys
):
    # Arrange
    weather_system.database.add_search_history.return_value = True

    with patch.object(
        WeatherSystem,
        "get_city_name_from_user",
        return_value="Athens"
    ), patch(
        "weathersystem.GeocodingApi.get_coordinates",
        return_value=(37.9838, 23.7275, "Athens", "GR")
    ) as mock_geocoding, patch(
        "weathersystem.WeatherApi.get_weather",
        return_value=sample_weather
    ) as mock_weather_api:

        # Act
        weather_system.display_weather()

    captured = capsys.readouterr()

    # Assert
    mock_geocoding.assert_called_once_with("Athens")

    mock_weather_api.assert_called_once_with(
        37.9838,
        23.7275
    )

    weather_system.database.add_search_history.assert_called_once()

    saved_history = (
        weather_system.database
        .add_search_history
        .call_args
        .args[0]
    )

    assert saved_history.city_name == "Athens"
    assert saved_history.country == "GR"

    assert "===== Current Weather =====" in captured.out
    assert "Athens" in captured.out
    assert "30.5" in captured.out


def test_display_weather_cancelled(weather_system):
    # Arrange
    with patch.object(
        WeatherSystem,
        "get_city_name_from_user",
        return_value=None
    ), patch(
        "weathersystem.GeocodingApi.get_coordinates"
    ) as mock_geocoding:

        # Act
        weather_system.display_weather()

    # Assert
    mock_geocoding.assert_not_called()
    weather_system.database.add_search_history.assert_not_called()


def test_display_weather_city_not_found(weather_system):
    # Arrange
    with patch.object(
        WeatherSystem,
        "get_city_name_from_user",
        return_value="Unknown"
    ), patch(
        "weathersystem.GeocodingApi.get_coordinates",
        return_value=(None, None, None, None)
    ), patch(
        "weathersystem.WeatherApi.get_weather"
    ) as mock_weather_api:

        # Act
        weather_system.display_weather()

    # Assert
    mock_weather_api.assert_not_called()
    weather_system.database.add_search_history.assert_not_called()


def test_display_weather_api_failure(weather_system):
    # Arrange
    with patch.object(
        WeatherSystem,
        "get_city_name_from_user",
        return_value="Athens"
    ), patch(
        "weathersystem.GeocodingApi.get_coordinates",
        return_value=(37.9838, 23.7275, "Athens", "GR")
    ), patch(
        "weathersystem.WeatherApi.get_weather",
        return_value=None
    ):

        # Act
        weather_system.display_weather()

    # Assert
    weather_system.database.add_search_history.assert_not_called()


def test_display_weather_search_history_not_saved(
    weather_system,
    sample_weather,
    capsys
):
    # Arrange
    weather_system.database.add_search_history.return_value = False

    with patch.object(
        WeatherSystem,
        "get_city_name_from_user",
        return_value="Athens"
    ), patch(
        "weathersystem.GeocodingApi.get_coordinates",
        return_value=(37.9838, 23.7275, "Athens", "GR")
    ), patch(
        "weathersystem.WeatherApi.get_weather",
        return_value=sample_weather
    ):

        # Act
        weather_system.display_weather()

    captured = capsys.readouterr()

    # Assert
    assert "The search could not be saved." in captured.out


def test_display_forecast_success(
    weather_system,
    capsys
):
    # Arrange
    forecast_day_1 = Weather(
        city="Athens",
        country="GR",
        temperature=30.0,
        feels_like=31.0,
        condition="Clear",
        description="clear sky",
        humidity=40,
        pressure=1013,
        wind_speed=3.0,
        date="2026-07-21"
    )

    forecast_day_2 = Weather(
        city="Athens",
        country="GR",
        temperature=31.0,
        feels_like=32.0,
        condition="Clouds",
        description="few clouds",
        humidity=42,
        pressure=1012,
        wind_speed=3.5,
        date="2026-07-22"
    )

    forecast_list = [
        forecast_day_1,
        forecast_day_2
    ]

    with patch.object(
        WeatherSystem,
        "get_city_name_from_user",
        return_value="Athens"
    ), patch(
        "weathersystem.GeocodingApi.get_coordinates",
        return_value=(37.9838, 23.7275, "Athens", "GR")
    ), patch(
        "weathersystem.WeatherApi.get_forecast",
        return_value=forecast_list
    ) as mock_forecast:

        # Act
        weather_system.display_forecast()

    captured = capsys.readouterr()

    # Assert
    mock_forecast.assert_called_once_with(
        37.9838,
        23.7275
    )

    assert "===== 5-Day Forecast =====" in captured.out
    assert "Date: 2026-07-21" in captured.out
    assert "Date: 2026-07-22" in captured.out
    assert "Athens" in captured.out


def test_display_forecast_cancelled(weather_system):
    # Arrange
    with patch.object(
        WeatherSystem,
        "get_city_name_from_user",
        return_value=None
    ), patch(
        "weathersystem.GeocodingApi.get_coordinates"
    ) as mock_geocoding:

        # Act
        weather_system.display_forecast()

    # Assert
    mock_geocoding.assert_not_called()


def test_display_forecast_city_not_found(weather_system):
    # Arrange
    with patch.object(
        WeatherSystem,
        "get_city_name_from_user",
        return_value="Unknown"
    ), patch(
        "weathersystem.GeocodingApi.get_coordinates",
        return_value=(None, None, None, None)
    ), patch(
        "weathersystem.WeatherApi.get_forecast"
    ) as mock_forecast:

        # Act
        weather_system.display_forecast()

    # Assert
    mock_forecast.assert_not_called()


def test_display_forecast_empty_list(
    weather_system,
    capsys
):
    # Arrange
    with patch.object(
        WeatherSystem,
        "get_city_name_from_user",
        return_value="Athens"
    ), patch(
        "weathersystem.GeocodingApi.get_coordinates",
        return_value=(37.9838, 23.7275, "Athens", "GR")
    ), patch(
        "weathersystem.WeatherApi.get_forecast",
        return_value=[]
    ):

        # Act
        weather_system.display_forecast()

    captured = capsys.readouterr()

    # Assert
    assert "===== 5-Day Forecast =====" not in captured.out


def test_display_air_quality_success(
    weather_system,
    sample_air_quality,
    capsys
):
    # Arrange
    with patch.object(
        WeatherSystem,
        "get_city_name_from_user",
        return_value="Athens"
    ), patch(
        "weathersystem.GeocodingApi.get_coordinates",
        return_value=(37.9838, 23.7275, "Athens", "GR")
    ), patch(
        "weathersystem.AirQualityApi.get_air_quality",
        return_value=sample_air_quality
    ) as mock_air_quality_api:

        # Act
        weather_system.display_air_quality()

    captured = capsys.readouterr()

    # Assert
    mock_air_quality_api.assert_called_once_with(
        37.9838,
        23.7275,
        "Athens",
        "GR"
    )

    assert "===== Air Quality =====" in captured.out
    assert "Athens" in captured.out
    assert "Fair" in captured.out


def test_display_air_quality_api_failure(
    weather_system,
    capsys
):
    # Arrange
    with patch.object(
        WeatherSystem,
        "get_city_name_from_user",
        return_value="Athens"
    ), patch(
        "weathersystem.GeocodingApi.get_coordinates",
        return_value=(37.9838, 23.7275, "Athens", "GR")
    ), patch(
        "weathersystem.AirQualityApi.get_air_quality",
        return_value=None
    ):

        # Act
        weather_system.display_air_quality()

    captured = capsys.readouterr()

    # Assert
    assert "===== Air Quality =====" not in captured.out


def test_save_favourite_city_success(
    weather_system,
    capsys
):
    # Arrange
    weather_system.database.add_favorite_city.return_value = True

    with patch.object(
        WeatherSystem,
        "get_city_name_from_user",
        return_value="Athens"
    ), patch(
        "weathersystem.GeocodingApi.get_coordinates",
        return_value=(37.9838, 23.7275, "Athens", "GR")
    ):

        # Act
        weather_system.save_favourite_city()

    captured = capsys.readouterr()

    # Assert
    weather_system.database.add_favorite_city.assert_called_once()

    saved_city = (
        weather_system.database
        .add_favorite_city
        .call_args
        .args[0]
    )

    assert isinstance(saved_city, FavoriteCity)
    assert saved_city.city_name == "Athens"
    assert saved_city.country == "GR"
    assert saved_city.latitude == 37.9838
    assert saved_city.longitude == 23.7275

    assert (
        "Athens,GR was  added to your favorite cities."
        in captured.out
    )


def test_save_favourite_city_duplicate(
    weather_system,
    capsys
):
    # Arrange
    weather_system.database.add_favorite_city.return_value = False

    with patch.object(
        WeatherSystem,
        "get_city_name_from_user",
        return_value="Athens"
    ), patch(
        "weathersystem.GeocodingApi.get_coordinates",
        return_value=(37.9838, 23.7275, "Athens", "GR")
    ):

        # Act
        weather_system.save_favourite_city()

    captured = capsys.readouterr()

    # Assert
    assert (
        "Athens,GR is already in your favorite cities."
        in captured.out
    )


def test_display_favorite_cities_weather_no_cities(
    weather_system,
    capsys
):
    # Arrange
    weather_system.database.get_all_favorite_cities.return_value = []

    # Act
    weather_system.display_favorite_cities_weather()

    captured = capsys.readouterr()

    # Assert
    assert "No favorite cities were found." in captured.out


def test_display_favorite_cities_weather_success(
    weather_system,
    sample_weather,
    capsys
):
    # Arrange
    favorite_city = FavoriteCity(
        city_name="Athens",
        country="GR",
        latitude=37.9838,
        longitude=23.7275,
        city_id=1
    )

    weather_system.database.get_all_favorite_cities.return_value = [
        favorite_city
    ]

    with patch(
        "weathersystem.WeatherApi.get_weather",
        return_value=sample_weather
    ) as mock_weather_api:

        # Act
        weather_system.display_favorite_cities_weather()

    captured = capsys.readouterr()

    # Assert
    mock_weather_api.assert_called_once_with(
        37.9838,
        23.7275
    )

    assert "===== Current Weather =====" in captured.out
    assert "Athens" in captured.out


def test_display_favorite_cities_weather_api_failure(
    weather_system,
    capsys
):
    # Arrange
    favorite_city = FavoriteCity(
        city_name="Athens",
        country="GR",
        latitude=37.9838,
        longitude=23.7275,
        city_id=1
    )

    weather_system.database.get_all_favorite_cities.return_value = [
        favorite_city
    ]

    with patch(
        "weathersystem.WeatherApi.get_weather",
        return_value=None
    ):

        # Act
        weather_system.display_favorite_cities_weather()

    captured = capsys.readouterr()

    # Assert
    assert (
        "Could not retrieve weather for Athens, GR."
        in captured.out
    )


def test_remove_fav_city_no_cities(
    weather_system,
    capsys
):
    # Arrange
    weather_system.database.get_all_favorite_cities.return_value = []

    # Act
    weather_system.remove_fav_city()

    captured = capsys.readouterr()

    # Assert
    assert "No favorite cities were found." in captured.out


def test_remove_fav_city_cancelled(
    weather_system,
    monkeypatch,
    capsys
):
    # Arrange
    favorite_city = FavoriteCity(
        city_name="Athens",
        country="GR",
        latitude=37.9838,
        longitude=23.7275,
        city_id=1
    )

    weather_system.database.get_all_favorite_cities.return_value = [
        favorite_city
    ]

    monkeypatch.setattr("builtins.input", lambda _: "0")

    # Act
    weather_system.remove_fav_city()

    captured = capsys.readouterr()

    # Assert
    assert "Operation cancelled." in captured.out
    weather_system.database.delete_favorite_city.assert_not_called()


def test_remove_fav_city_invalid_inputs_then_success(
    weather_system,
    monkeypatch,
    capsys
):
    # Arrange
    favorite_city = FavoriteCity(
        city_name="Athens",
        country="GR",
        latitude=37.9838,
        longitude=23.7275,
        city_id=1
    )

    weather_system.database.get_all_favorite_cities.return_value = [
        favorite_city
    ]

    weather_system.database.get_favorite_city_by_id.side_effect = [
        None,
        favorite_city
    ]

    weather_system.database.delete_favorite_city.return_value = True

    user_inputs = iter([
        "abc",
        "-1",
        "99",
        "1"
    ])

    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(user_inputs)
    )

    # Act
    weather_system.remove_fav_city()

    captured = capsys.readouterr()

    # Assert
    assert "Please enter a numeric city ID." in captured.out
    assert "Please enter a valid city ID." in captured.out

    assert (
        "No favorite city with this ID was found."
        in captured.out
    )

    weather_system.database.delete_favorite_city.assert_called_once_with(
        favorite_city
    )

    assert (
        "Athens, GR was removed from your favorite cities."
        in captured.out
    )


def test_remove_fav_city_delete_failure(
    weather_system,
    monkeypatch,
    capsys
):
    # Arrange
    favorite_city = FavoriteCity(
        city_name="Athens",
        country="GR",
        latitude=37.9838,
        longitude=23.7275,
        city_id=1
    )

    weather_system.database.get_all_favorite_cities.return_value = [
        favorite_city
    ]

    weather_system.database.get_favorite_city_by_id.return_value = (
        favorite_city
    )

    weather_system.database.delete_favorite_city.return_value = False

    monkeypatch.setattr("builtins.input", lambda _: "1")

    # Act
    weather_system.remove_fav_city()

    captured = capsys.readouterr()

    # Assert
    assert (
        "The favorite city could not be removed."
        in captured.out
    )


def test_display_search_history_no_history(
    weather_system,
    capsys
):
    # Arrange
    weather_system.database.get_search_history.return_value = []

    # Act
    weather_system.display_search_history()

    captured = capsys.readouterr()

    # Assert
    assert "No search history was found." in captured.out


def test_display_search_history_success(
    weather_system,
    capsys
):
    # Arrange
    first_history = Mock()
    first_history.__str__ = Mock(
        return_value="1. Athens, GR - 2026-07-20"
    )

    second_history = Mock()
    second_history.__str__ = Mock(
        return_value="2. London, GB - 2026-07-19"
    )

    weather_system.database.get_search_history.return_value = [
        first_history,
        second_history
    ]

    # Act
    weather_system.display_search_history()

    captured = capsys.readouterr()

    # Assert
    assert "===== Search History =====" in captured.out
    assert "Athens, GR" in captured.out
    assert "London, GB" in captured.out