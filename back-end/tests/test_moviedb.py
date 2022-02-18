import moviedb
import pytest


@pytest.fixture()
def movies():
    yield moviedb.MovieDb()


def test_movies_search(movies):
    results = movies.search("Three Amigos! (1986)")
    assert len(results) > 5


def test_get_title(movies):
    title = movies.get_title("0092086")
    assert title


def test_get_rating(movies):
    rating = movies.get_rating("0092086")
    assert rating == moviedb.Certification.PG


def test_get_synopsis(movies):
    synopsis = movies.get_synopsis("0092086")
    assert (
        synopsis
        == "Three actors accept an invitation to a Mexican village to perform their onscreen bandit fighter roles, unaware that it is the real thing."
    )
