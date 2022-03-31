from fastapi import FastAPI
from .routers import users, movies


def create_app():
    app = FastAPI()

    app.include_router(users.router)
    app.include_router(movies.router)

    return app
