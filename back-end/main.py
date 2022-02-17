import logging

from fastapi import FastAPI

import feature_flags
from routers import movie

logging.basicConfig(level=logging.INFO)
app = FastAPI()
app.include_router(movie.router, prefix="/movie")


@app.on_event("startup")
def on_startup():
    feature_flags.init()


@app.get("/")
async def home():
    return {"hello": "world"}
