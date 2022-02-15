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


@pytest.mark.parametrize("flag_state, expected", [(True, 200), (False, 404)])
def test_get_synopsis(synopsis_flag_on, flag_state, expected, client):
    response = client.get("/movie/0092086/synopsis")
    assert response.status_code == expected
    if flag_state:  # flag enabled
        assert response.json()["data"]["plot"]
