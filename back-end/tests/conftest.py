from os import environ

import pytest
import requests


class FeatureFlagOn:
    def __init__(self, on_url: str) -> None:
        self.on_url = on_url

    def __enter__(self):
        resp = requests.post(url=self.on_url)
        assert resp.status_code == 200

    def __exit__(self, exc_type, exc_value, exc_traceback):
        # TODO: restore the flag??
        pass


class FeatureFlagOff:
    def __init__(self, off_url: str) -> None:
        self.off_url = off_url

    def __enter__(self):
        resp = requests.post(url=self.off_url)
        assert resp.status_code == 200

    def __exit__(self, exc_type, exc_value, exc_traceback):
        # TODO: restore the flag??
        pass


@pytest.fixture(scope="function")
def synopsis_flag_on(flag_state: bool):
    if flag_state:
        with FeatureFlagOn(environ["SYNOPSIS_TRIGGER_ON_URL"]):
            yield
    else:
        with FeatureFlagOff(environ["SYNOPSIS_TRIGGER_OFF_URL"]):
            yield
