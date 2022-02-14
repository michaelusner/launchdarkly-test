from enum import Enum
from typing import List

from imdb import IMDb


class Certification(Enum):
    TVG = "United States:TV-G"
    G = "United States:G"
    PG = "United States:PG"
    R = "United States:R"
    UNRATED = "United States:Unrated"
    PG13 = "United States:PG-13"


class MovieDb:
    def __init__(self) -> None:
        self.client = IMDb()

    def search(self, name: str) -> List:
        return self.client.search_movie(name)

    def get_rating(self, movie_id: str, region: str = "United States") -> Certification:
        ret = self.client.get_movie_parents_guide(movie_id)
        return Certification(
            [i.strip() for i in ret["data"]["certification"] if "United States" in i][0]
        )
