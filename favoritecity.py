class FavoriteCity:
    def __init__(
        self,
        city_name,
        country,
        latitude,
        longitude,
        city_id=None
    ):
        self.city_name = city_name
        self.country = country
        self.latitude = latitude
        self.longitude = longitude
        self.city_id = city_id

    def __str__(self):
        return f"{self.city_id}. {self.city_name}, {self.country}"