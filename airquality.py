class AirQuality:
    def __init__(self,city,country,aqi,quality,pm2_5,pm10,co,no2,o3):
        self.city = city
        self.country = country
        self.aqi = aqi
        self.quality = quality
        self.pm2_5 = pm2_5
        self.pm10 = pm10
        self.co = co
        self.no2 = no2
        self.o3 = o3

    def __str__(self):
        return (
            f"City             : {self.city}\n"
            f"Country          : {self.country}\n\n"
            f"AQI              : {self.aqi}\n"
            f"Quality          : {self.quality}\n\n"
            f"PM2.5            : {self.pm2_5:.2f} μg/m³\n"
            f"PM10             : {self.pm10:.2f} μg/m³\n"
            f"Carbon Monoxide  : {self.co:.2f} μg/m³\n"
            f"Nitrogen Dioxide : {self.no2:.2f} μg/m³\n"
            f"Ozone            : {self.o3:.2f} μg/m³"
        )
