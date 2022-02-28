# Copyright 2022 - Hewlett Packard Enterprise Company
"""
LaunchDarkly feature flag module

This module depends on the launchdarkly-server-sdk "ldclient" module.  The ldclient
ensures that the underlying LDClient instance remains a singleton (see the docs
for more info: https://docs.launchdarkly.com/sdk/server-side/python)
Rather than incorporate ldclient in your code itself, this module provides a
convenience function and context manager to allow incorporation of LaunchDarkly
in a simple and consistent manner.  Both methods wrap the ldclient.init() function
but still require the end user to call close() at the closing of the application.

Usage:
    * flag() function
        The flag function allows you to query a feature flag in the traditional if/else
        model:
        if flag(key=<flag key>, user=<user>, default=<default>) == <expected value>:
            code...
        else:
            code...

    * FeatureFlag context manager can be used as traditional FastAPI dependency


Default values:


"""
import hashlib
import logging
from functools import wraps
from os import environ
from typing import Optional, TypeVar

import ldclient  # type: ignore
from fastapi import Header, HTTPException
from fastapi.params import Header as HeaderCls
from ldclient.config import Config  # type: ignore

T = TypeVar("T")  # used to ensure consistent typing of default values in flags

logger = logging.getLogger(__name__)


def init(**kwargs):
    # Do not import ldclient directly in your code
    # (https://docs.launchdarkly.com/sdk/server-side/python)
    # ldclient must be a singleton
    # It's important to make ldclient a singleton. The client instance maintains
    # internal state that allows LaunchDarkly to serve feature flags without making any
    # remote requests. Do not instantiate a new client with every request.
    sdk_key = environ.get("LAUNCHDARKLY_SDK_KEY", "unset")
    ldclient.set_config(
        Config(
            sdk_key,
            offline=True if sdk_key == "unset" else False,
            **kwargs,
        )
    )


def flag(key: str, user: dict, default: T = None) -> T:
    """
    LaunchDarkly feature flag
    Usage:
    if feature_flags.flag(key="your_flag", user=<ld_user>, default=<default value)):
        code...
    else:
        code...

    Note that <default value> will be used in the event that either the client
    cannot connect to LaunchDarkly, or the flag doesn't exist.
    """
    if ldclient.__config is None:
        init()
    return ldclient.get().variation(key=key, user=user, default=default)


def close():
    """
    Close should be called when your application terminates
    Add to FastAPI app.on_event("shutdown")

    """
    if ldclient.__config:
        ldclient.get().close()


class FeatureFlag:
    """
    Feature flag base class
    """

    def __init__(self, key: str, user: dict, default: T = None) -> None:
        self.key = key
        self.user = user
        self.default = default

    def __enter__(self, *args, **kwargs):
        return flag(self.key, self.user, self.default)

    def __exit__(self, exc_type, exc_value, exc_traceback):
        # __exit__ is required but not used
        pass


def get_launchdarkly_user(
    cid: Optional[str] = Header(default=None, alias="rugby-cid"),
    email: Optional[str] = Header(default=None, alias="rugby-user-email"),
) -> dict:
    # allow calling this function directly, without fastapi Depends()
    if isinstance(email, HeaderCls):
        email = email.default
    if isinstance(cid, HeaderCls):
        cid = cid.default

    to_return: dict
    if email or cid:
        # match the customer id used by the API gateway when token validation is disabled
        cid = cid or "aci1"
        email = email or "anonymous"
        key_str = email + ":" + cid
        key = hashlib.sha256(key_str.encode("UTF-8")).hexdigest()

        to_return = {
            "key": key,
            "custom": {
                "cid": cid,
            },
        }
        if email in {"nobody@nowhere", "anonymous"} or email.endswith("@hpe.com"):
            to_return["email"] = email
    else:
        to_return = {"key": "anonymous", "anonymous": True}

    logger.debug("Using LD user %s", to_return)
    return to_return


def route_feature_flag(key, value, raise_on_disabled=True):
    def flag_deco(func):
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            with FeatureFlag(
                key=key,
                default=value,
                user=kwargs.get("user"),
            ) as flag:
                if flag != value:
                    raise HTTPException(status_code=404)
                return await func(*args, **kwargs)

        return async_wrapper

    return flag_deco
