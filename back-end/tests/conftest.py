import logging
from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient
from feature_flags import FeatureFlag
from main import app

logging.basicConfig(level=logging.INFO)
anonymous_user = {"key": "pytest", "anonymous": True}


@pytest.fixture
def http_client():
    with TestClient(app) as client:
        yield client


@pytest.fixture(scope="function")
def mock_feature_flag(request):
    marker = request.node.get_closest_marker("mock_feature_flag")
    if "key" not in marker.kwargs:
        raise AssertionError("mock_feature_flag: no flag key provided")
    if "value" not in marker.kwargs:
        raise AssertionError("mock_feature_flag: no flag value provided")
    with patch("ldclient.LDClient", autospec=True) as client:
        client.return_value.variation.return_value = marker.kwargs["value"]
        yield marker.kwargs["value"]


@pytest.fixture(scope="function")
def feature_flag(request):
    marker = request.node.get_closest_marker("feature_flag")
    if "key" not in marker.kwargs:
        raise AssertionError("feature_flag: no flag key provided")
    with FeatureFlag(
        key=marker.kwargs["key"],
        user=marker.kwargs.get("user", anonymous_user),
        default=marker.kwargs.get("default"),
    ) as flag:
        if "value" in marker.kwargs and marker.kwargs["value"] != flag:
            pytest.skip(
                "feature_flag: skipping test due to "
                + f"{marker.kwargs.get('key')}={marker.kwargs.get('value')}"
            )
        yield flag
