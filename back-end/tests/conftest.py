import logging
from typing import Any
from unittest.mock import patch

import feature_flags
import pytest
from fastapi.testclient import TestClient
from main import app

logging.basicConfig(level=logging.INFO)
anonymous_user = {"key": "pytest", "email": "anonymous"}


@pytest.fixture
def http_client():
    with TestClient(app) as client:
        yield client


feature_flag_values = dict()


def get_variation(key: str, user: dict, default: Any):
    return feature_flag_values[key]


@pytest.fixture
def mock_feature_flag(request):
    marker = request.node.get_closest_marker("mock_feature_flag")
    if "key" not in marker.kwargs:
        raise AssertionError("mock_feature_flag: no flag key provided")
    if "value" not in marker.kwargs:
        raise AssertionError("mock_feature_flag: no flag value provided")
    feature_flag_values[marker.kwargs["key"]] = marker.kwargs["value"]
    with patch("ldclient.LDClient", autospec=True) as client:
        logging.info("%s = %s", marker.kwargs["key"], marker.kwargs["value"])
        client.return_value.variation = get_variation
        yield marker.kwargs["value"]


@pytest.fixture(scope="session")
def feature_flag_session():
    feature_flags.init()
    yield
    feature_flags.close()


@pytest.fixture
def feature_flag(feature_flag_session, request):
    marker = request.node.get_closest_marker("feature_flag")
    if "key" not in marker.kwargs:
        raise AssertionError("feature_flag: no flag key provided")
    flag_value = feature_flags.flag(
        key=marker.kwargs["key"],
        user=marker.kwargs.get(
            "user",
            feature_flags.get_launchdarkly_user(
                cid=request.node.name, email="anonymous"
            ),
        ),
        default=marker.kwargs.get("default"),
    )
    if "value" in marker.kwargs and marker.kwargs["value"] != flag_value:
        pytest.skip(
            "feature_flag: skipping test due to "
            + f"{marker.kwargs.get('key')}={marker.kwargs.get('value')}"
        )
    yield flag_value
