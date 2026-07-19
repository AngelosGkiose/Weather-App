import sqlite3

from favoritecity import FavoriteCity


class Database:
    def __init__(self):
        self.connection = sqlite3.connect("favourite_city.db")
        self.cursor = self.connection.cursor()
        self.create_table()


    def create_table(self):
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS favorite_cities (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    city_name TEXT NOT NULL,
    country TEXT NOT NULL,
    latitude REAL NOT NULL,
    longitude REAL NOT NULL,
    UNIQUE(city_name, country)
)""")
        self.connection.commit()

    def add_favorite_city(self, favorite_city):
        try:
            self.cursor.execute(
                """
                INSERT INTO favorite_cities (
                    city_name,
                    country,
                    latitude,
                    longitude
                )
                VALUES (?, ?, ?, ?)
                """,
                (
                    favorite_city.city_name,
                    favorite_city.country,
                    favorite_city.latitude,
                    favorite_city.longitude
                )
            )
            favorite_city.city_id = self.cursor.lastrowid
            self.connection.commit()
            return True
        except sqlite3.IntegrityError:
            self.connection.rollback()
            return False

    def get_favorite_city(self):
        self.cursor.execute("SELECT * FROM favorite_cities")
        rows= self.cursor.fetchall()
        favorite_city = []
        for row in rows:
            favorite_city.append(FavoriteCity(row[1], row[2], row[3], row[4],row[0]))
        return favorite_city

