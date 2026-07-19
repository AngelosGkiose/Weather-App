class SearchHistory:
    def __init__(self,city_name,country,search_date,history_id=None):
        self.city_name = city_name
        self.country = country
        self.search_date = search_date
        self.history_id = history_id

    def __str__(self):
        return (
            f"{self.history_id}. {self.city_name}, {self.country}\n"
            f"   Searched on: {self.search_date}"
        )