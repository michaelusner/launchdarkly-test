import moviedb
import pytest


@pytest.fixture()
def movies():
    yield moviedb.MovieDb()


def test_movies_search(movies):
    results = movies.search("Three Amigos! (1986)")
    assert len(results) > 5


def test_get_rating(movies):
    rating = movies.get_rating("0092086")
    assert rating == moviedb.Certification.PG


def test_get_synopsis(movies):
    synopsis = movies.get_synopsis("0092086")
    assert len(synopsis["data"]["plot"])
