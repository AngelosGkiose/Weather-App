class Weather:
    def __init__(
        self,
        city,
        country,
        temperature,
        feels_like,
        condition,
        description,
        humidity,
        pressure,
        wind_speed,
        date=None
    ):
        self.city = city
        self.country = country
        self.temperature = temperature
        self.feels_like = feels_like
        self.condition = condition
        self.description = description
        self.humidity = humidity
        self.pressure = pressure
        self.wind_speed = wind_speed
        self.date = date
        
    def __str__(self):
        return (
            f"City         : {self.city}\n"
            f"Country      : {self.country}\n\n"
            f"Temperature  : {self.temperature:.1f} °C\n"
            f"Feels Like   : {self.feels_like:.1f} °C\n\n"
            f"Condition    : {self.condition}\n"
            f"Description  : {self.description.title()}\n\n"
            f"Humidity     : {self.humidity}%\n"
            f"Pressure     : {self.pressure} hPa\n"
            f"Wind Speed   : {self.wind_speed:.1f} m/s"
        )