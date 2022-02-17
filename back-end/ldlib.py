import atexit
import logging
from functools import wraps
from os import environ
from typing import Any

import ldclient
from fastapi import HTTPException, status
from ldclient.config import Config
from pydantic import BaseModel

# TODO: create an init function here that creates the ldclient
# TODO: provide mock for unit/component tests
# TODO: consider caching scenarios

logging.basicConfig(level=logging.INFO)


def feature_flag_init():
    global blah


# ldclient must be a singleton.  Do not create more ldclient instances.
ldclient.set_config(Config(environ["LAUNCHDARKLY_KEY"]))
feature_flag_client = ldclient.get()

# register a handler to close the flag client on exit
atexit.register(lambda: feature_flag_client.close())


class FeatureFlag:
    def __init__(self, key: str, user: dict, default: Any = None) -> None:
        self.key = key
        self.user = user
        self.default = default

    def __enter__(self):
        return feature_flag_client.variation(
            key=self.key, user=self.user, default=self.default
        )

    def __exit__(self, exc_type, exc_value, exc_traceback):
        # do nothing
        pass


class FeatureFlagEnabled:
    def __init__(self, key: str, user: dict):
        self.key = key
        self.user = user

    def __enter__(self):
        with FeatureFlag(key=self.key, user=self.user) as flag:
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
            with FeatureFlagEnabled(
                key=key, user={"key": kwargs["user"].customer_id, "anonymous": False}
            ):
                return await func(*args, **kwargs)

        return wrapper

    return flag_deco


# with FeatureFlag(key='something') as data:
# code with data
