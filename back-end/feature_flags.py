import logging
from functools import wraps
from os import environ
from typing import Union

import ldclient as __ldclient
from fastapi import HTTPException, status
from ldclient.config import Config
from pydantic import BaseModel

# TODO: create an init function here that creates the ldclient
# TODO: provide mock for unit/component tests
# TODO: consider caching scenarios

logging.basicConfig(level=logging.INFO)


class FeatureError(Exception):
    pass


def init(**kwargs):
    # ldclient should be shared.  Do not import ldclient directly in your code.
    __ldclient.set_config(
        Config(
            environ["LAUNCHDARKLY_KEY"],
            base_uri=environ.get("LAUNCHDARKLY_URI", "https://app.launchdarkly.com"),
            events_uri=environ.get(
                "LAUNCHDARKLY_EVENTS_URI", "https://events.launchdarkly.com"
            ),
            stream_uri=environ.get(
                "LAUNCHDARKLY_STREAM_URI", "https://stream.launchdarkly.com"
            ),
            **kwargs,
        )
    )


def flag(key: str, user: dict, default: None):
    if __ldclient.__config is None:
        init()
    with __ldclient.get() as client:
        return client.variation(key=key, user=user, default=default)


def close():
    if __ldclient.__config:
        __ldclient.get().close()


class Flag:
    def __init__(
        self, key: str, user: dict, default: Union[bool, int, str, dict] = None
    ) -> None:
        self.key = key
        self.user = user
        self.default = default

    def __enter__(self):
        return flag(key=self.key, user=self.user, default=self.default)

    def __exit__(self, exc_type, exc_value, exc_traceback):
        x = 5


class FlagRequired:
    def __init__(self, key: str, user: dict):
        self.key = key
        self.user = user

    def __enter__(self):
        with Flag(key=self.key, user=self.user) as flag:
            logging.info("%s flag is %s", self.key, flag)
            if not flag:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Feature flag {self.key} is False",
                )

    def __exit__(self, exc_type, exc_value, exc_traceback):
        # do nothing
        pass


class User(BaseModel):
    email: str
    first: str
    last: str
    customer_id: str
    permissions: list


def get_authenticated_user():
    return User(
        email="testuser@test.com",
        first="Test",
        last="User",
        customer_id="abcd123",
        permissions=[],
    )


def feature_flag(key):
    def flag_deco(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            with FlagRequired(
                key=key, user={"key": kwargs["user"].customer_id, "anonymous": False}
            ):
                return await func(*args, **kwargs)

        return wrapper

    return flag_deco
