import pytest

from database import Database
from favoritecity import FavoriteCity
from searchhistory import SearchHistory


@pytest.fixture
def database():
    db = Database(":memory:")

    yield db

    db.connection.close()


def test_add_favorite_city(database):

    favorite_city = FavoriteCity(
        city_name="Athens",
        country="GR",
        latitude=37.9838,
        longitude=23.7275
    )

    result = database.add_favorite_city(favorite_city)

    assert result is True
    assert favorite_city.city_id is not None


def test_get_all_favorite_cities(database):

    favorite_city = FavoriteCity(
        city_name="Athens",
        country="GR",
        latitude=37.9838,
        longitude=23.7275
    )

    database.add_favorite_city(favorite_city)


    favorite_cities = database.get_all_favorite_cities()


    assert len(favorite_cities) == 1

    saved_city = favorite_cities[0]

    assert saved_city.city_name == "Athens"
    assert saved_city.country == "GR"
    assert saved_city.latitude == 37.9838
    assert saved_city.longitude == 23.7275
    assert saved_city.city_id is not None


def test_add_duplicate_favorite_city_returns_false(database):

    first_city = FavoriteCity(
        city_name="Athens",
        country="GR",
        latitude=37.9838,
        longitude=23.7275
    )

    duplicate_city = FavoriteCity(
        city_name="Athens",
        country="GR",
        latitude=37.9838,
        longitude=23.7275
    )

    database.add_favorite_city(first_city)


    result = database.add_favorite_city(duplicate_city)


    assert result is False
    assert len(database.get_all_favorite_cities()) == 1


def test_delete_favorite_city(database):

    favorite_city = FavoriteCity(
        city_name="Athens",
        country="GR",
        latitude=37.9838,
        longitude=23.7275
    )

    database.add_favorite_city(favorite_city)


    result = database.delete_favorite_city(favorite_city)


    assert result is True
    assert database.get_all_favorite_cities() == []


def test_delete_nonexistent_favorite_city_returns_false(database):

    favorite_city = FavoriteCity(
        city_name="Athens",
        country="GR",
        latitude=37.9838,
        longitude=23.7275
    )


    result = database.delete_favorite_city(favorite_city)

    assert result is False


def test_get_favorite_city_by_id(database):

    favorite_city = FavoriteCity(
        city_name="Athens",
        country="GR",
        latitude=37.9838,
        longitude=23.7275
    )

    database.add_favorite_city(favorite_city)

    saved_city = database.get_favorite_city_by_id(
        favorite_city.city_id
    )


    assert saved_city is not None
    assert saved_city.city_id == favorite_city.city_id
    assert saved_city.city_name == "Athens"
    assert saved_city.country == "GR"


def test_get_favorite_city_by_invalid_id_returns_none(database):

    result = database.get_favorite_city_by_id(999)


    assert result is None


def test_add_search_history(database):

    history = SearchHistory(
        city_name="Athens",
        country="GR",
        search_date="2026-07-20"
    )


    result = database.add_search_history(history)


    assert result is True
    assert history.history_id is not None


def test_get_search_history(database):

    history = SearchHistory(
        city_name="Athens",
        country="GR",
        search_date="2026-07-20"
    )

    database.add_search_history(history)


    results = database.get_search_history()


    assert len(results) == 1
    assert results[0].city_name == "Athens"
    assert results[0].country == "GR"
    assert results[0].search_date == "2026-07-20"


def test_search_history_is_ordered_descending(database):

    first = SearchHistory(
        city_name="Athens",
        country="GR",
        search_date="2026-07-20"
    )

    second = SearchHistory(
        city_name="London",
        country="UK",
        search_date="2026-07-21"
    )

    database.add_search_history(first)
    database.add_search_history(second)


    history = database.get_search_history()


    assert len(history) == 2
    assert history[0].city_name == "London"
    assert history[1].city_name == "Athens"