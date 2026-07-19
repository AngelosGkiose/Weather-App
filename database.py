import sqlite3

from favoritecity import FavoriteCity
from searchhistory import SearchHistory


class Database:
    def __init__(self):
        self.connection = sqlite3.connect("favourite_city.db")
        self.cursor = self.connection.cursor()
        self.create_table()
        self.create_table_search_history()


    def create_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS favorite_cities (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                city_name TEXT NOT NULL,
                country TEXT NOT NULL,
                latitude REAL NOT NULL,
                longitude REAL NOT NULL,
                UNIQUE(city_name, country)
        )
        """
        )
        self.connection.commit()

    def create_table_search_history(self):
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS search_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                city_name TEXT NOT NULL,
                country TEXT NOT NULL,
                date TEXT NOT NULL
            )
            """
        )
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

    def get_all_favorite_cities(self):
        self.cursor.execute(
            """
            SELECT id, city_name, country, latitude, longitude
            FROM favorite_cities
            ORDER BY city_name
            """
        )
        rows = self.cursor.fetchall()
        favorite_cities = []
        for row in rows:
            favorite_cities.append(
                FavoriteCity(
                    city_name=row[1],
                    country=row[2],
                    latitude=row[3],
                    longitude=row[4],
                    city_id=row[0]
                )
            )
        return favorite_cities

    def get_favorite_city_by_id(self, city_id):
        self.cursor.execute("SELECT * FROM favorite_cities WHERE id = ?", (city_id,))
        row=self.cursor.fetchone()
        if row is None:
            return None
        return FavoriteCity(row[1], row[2], row[3], row[4], row[0])

    def delete_favorite_city(self, city):
        try:
            self.cursor.execute("DELETE FROM favorite_cities "
                                "WHERE city_name = ? and country=?",
                                (city.city_name, city.country))
            self.connection.commit()
            return self.cursor.rowcount > 0
        except sqlite3.IntegrityError:
            self.connection.rollback()
            return False

    def add_search_history(self, search_history):
        try:
            self.cursor.execute(
                """
                INSERT INTO search_history (
                    city_name,
                    country,
                    date
                )
                VALUES (?, ?, ?)
                """,
                (
                    search_history.city_name,
                    search_history.country,
                    search_history.search_date
                )
            )
            search_history.history_id = self.cursor.lastrowid
            self.connection.commit()
            return True
        except sqlite3.Error:
            self.connection.rollback()
            return False

    def get_search_history(self):
        self.cursor.execute("SELECT * FROM search_history  ORDER BY id DESC")
        rows = self.cursor.fetchall()
        search_history = []
        for row in rows:
            search_history.append(SearchHistory(row[1], row[2], row[3],row[0]))
        return search_history