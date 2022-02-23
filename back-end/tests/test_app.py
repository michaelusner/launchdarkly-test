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


@pytest.mark.mock_feature_flag(key="SHOW_SYNOPSIS", value=True)
def test_synopsis_feature_on_should_200(mock_feature_flag, http_client):
    with http_client.get("/movie/0092086/synopsis") as resp:
        assert resp.status_code == 200
        assert (
            resp.text
            == '"Three actors accept an invitation to a Mexican village to perform their onscreen bandit fighter roles, unaware that it is the real thing."'
        )


@pytest.mark.mock_feature_flag(key="SHOW_SYNOPSIS", value=False)
def test_synopsis_feature_off_should_404(mock_feature_flag, http_client):
    with http_client.get("/movie/0092086/synopsis") as resp:
        assert resp.status_code == 404


@pytest.mark.mock_feature_flag(key="test_string_flag", value="variation2")
def test_variation(mock_feature_flag):
    assert mock_feature_flag == "variation2"
