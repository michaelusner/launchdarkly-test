import pytest
from fastapi.testclient import TestClient
from main import app
from moviedb import Certification


@pytest.fixture
def client():
    yield TestClient(app)


def test_get_rating(client):
    response = client.get("/movie/0092086/rating")
    assert response.status_code == 200
    assert Certification(response.json()) == Certification.PG


@pytest.mark.feature_flag(key="T_20220217_1234_SHOW_MOVIE_SYNOPSIS", value=True)
def test_synopsis(feature_flag, http_client):
    with http_client.get("/movie/0092086/synopsis") as resp:
        assert resp.status_code == 200
        assert (
            resp.text
            == '"Three actors accept an invitation to a Mexican village to perform their onscreen bandit fighter roles, unaware that it is the real thing."'
        )


@pytest.mark.feature_flag(key="T_20220217_1234_SHOW_MOVIE_SYNOPSIS", value=False)
def test_synopsis_fails(feature_flag, http_client):
    with http_client.get("/movie/0092086/synopsis") as resp:
        assert resp.status_code == 404


@pytest.mark.feature_flag(key="test_string_flag", value="variation2")
def test_variation(feature_flag):
    assert feature_flag == "variation2"
