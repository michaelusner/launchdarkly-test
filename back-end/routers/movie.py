from fastapi import APIRouter, Depends, Request, Response
from feature_flags import User, get_authenticated_user, route_feature_flag
from moviedb import MovieDb

router = APIRouter(tags=["Movie"])


@router.get("/{movie_id}/title")
async def get_title(movie_id: str):
    return MovieDb().get_title(movie_id=movie_id)


@router.get("/{movie_id}/rating")
async def get_rating(movie_id: str):
    return MovieDb().get_rating(movie_id=movie_id)


@router.get("/{movie_id}/synopsis")
@route_feature_flag(key="SHOW_SYNOPSIS", value=True)
async def get_synopsis(
    movie_id: str,
    request: Request,
    response: Response,
    user: User = Depends(get_authenticated_user),
):
    return MovieDb().get_synopsis(movie_id=movie_id)
