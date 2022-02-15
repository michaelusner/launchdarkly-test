import atexit
from os import environ
from typing import Any

import ldclient
from ldclient.config import Config

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
