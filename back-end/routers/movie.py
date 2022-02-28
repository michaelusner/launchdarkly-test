import feature_flags
from fastapi import APIRouter, Depends, Request, Response
from moviedb import MovieDb

router = APIRouter(tags=["Movie"])


@router.get("/{movie_id}/title")
async def get_title(movie_id: str):
    return MovieDb().get_title(movie_id=movie_id)


@router.get("/{movie_id}/rating")
async def get_rating(movie_id: str):
    return MovieDb().get_rating(movie_id=movie_id)


@router.get("/{movie_id}/synopsis")
@feature_flags.route_feature_flag(key="TEST_FEATURE_FLAG", value=True)
async def get_synopsis(
    movie_id: str,
    request: Request,
    response: Response,
    user=Depends(feature_flags.get_launchdarkly_user),
):
    return MovieDb().get_synopsis(movie_id=movie_id)
