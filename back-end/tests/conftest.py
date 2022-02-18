from enum import Enum

import pytest
from fastapi.testclient import TestClient
from feature_flags import Flag
from main import app

anonymous_user = {"key": "pytest", "anonymous": True}


@pytest.fixture
def http_client():
    with TestClient(app) as client:
        yield client


@pytest.fixture
def feature_flag(request):
    marker = request.node.get_closest_marker("feature_flag")
    if marker is None:
        raise AssertionError("feature_flag: no flag key provided")
    with Flag(
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
