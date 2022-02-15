from functools import wraps

from fastapi import APIRouter, Depends, Request, Response, status
from fastapi.exceptions import HTTPException
from ldlib import FeatureFlag
from moviedb import MovieDb
from pydantic import BaseModel

router = APIRouter(tags=["Movie"])


@router.get("/{movie_id}/rating")
async def get_rating(movie_id: str):
    return MovieDb().get_rating(movie_id=movie_id)


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


class FeatureFlagEnabled:
    def __init__(self, key: str, user: dict):
        self.key = key
        self.user = user

    def __enter__(self):
        with FeatureFlag(key=self.key, user=self.user) as flag:
            if not flag:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Feature flag {self.key} is False",
                )

    def __exit__(self, exc_type, exc_value, exc_traceback):
        # do nothing
        pass


def feature_flag(key):
    def flag_deco(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            with FeatureFlagEnabled():
                return await func(*args, **kwargs)

        return wrapper

    return flag_deco


@router.get("/{movie_id}/synopsis")
@feature_flag(key="musner_movie_synopsis_1_20220214")
async def get_synopsis(
    movie_id: str,
    request: Request,
    response: Response,
    user: User = Depends(get_authenticated_user),
):
    return MovieDb().get_synopsis(movie_id=movie_id)
