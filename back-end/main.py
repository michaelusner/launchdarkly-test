import logging

from fastapi import FastAPI

from routers import movie

logging.basicConfig(level=logging.INFO)
app = FastAPI()
app.include_router(movie.router, prefix="/movie")


@app.get("/")
async def home():
    return {"hello": "world"}
