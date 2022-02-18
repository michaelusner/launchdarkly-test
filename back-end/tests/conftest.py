from os import environ

import pytest
from feature_flags import Flag, init


@pytest.fixture(scope="function")
def synopsis_flag_on(flag_state: bool):
    if flag_state:
        with Flag(environ["SYNOPSIS_TRIGGER_ON_URL"]):
            yield
    else:
        with FeatureFlagOff(environ["SYNOPSIS_TRIGGER_OFF_URL"]):
            yield
