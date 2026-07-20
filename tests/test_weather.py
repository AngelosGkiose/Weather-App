from weather import Weather


def test_weather_creation():

    city = "Athens"
    country = "GR"
    temperature = 30.5
    feels_like = 32.0
    condition = "Clear"
    description = "clear sky"
    humidity = 40
    pressure = 1013
    wind_speed = 3.5
    date = "2026-07-20"


    weather = Weather(
        city,
        country,
        temperature,
        feels_like,
        condition,
        description,
        humidity,
        pressure,
        wind_speed,
        date
    )


    assert weather.city == "Athens"
    assert weather.country == "GR"
    assert weather.temperature == 30.5
    assert weather.feels_like == 32.0
    assert weather.condition == "Clear"
    assert weather.description == "clear sky"
    assert weather.humidity == 40
    assert weather.pressure == 1013
    assert weather.wind_speed == 3.5
    assert weather.date == "2026-07-20"


def test_weather_date_is_none_by_default():

    weather = Weather(
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


    result = weather.date


    assert result is None


def test_weather_string_representation():

    weather = Weather(
        city="Athens",
        country="GR",
        temperature=30.56,
        feels_like=32.04,
        condition="Clear",
        description="clear sky",
        humidity=40,
        pressure=1013,
        wind_speed=3.54
    )

    expected_result = (
        "City         : Athens\n"
        "Country      : GR\n\n"
        "Temperature  : 30.6 °C\n"
        "Feels Like   : 32.0 °C\n\n"
        "Condition    : Clear\n"
        "Description  : Clear Sky\n\n"
        "Humidity     : 40%\n"
        "Pressure     : 1013 hPa\n"
        "Wind Speed   : 3.5 m/s"
    )


    result = str(weather)


    assert result == expected_result