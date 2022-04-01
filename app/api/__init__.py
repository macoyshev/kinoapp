from fastapi import FastAPI

from .routers import movies, users


def create_app() -> FastAPI:
    app = FastAPI()

    app.include_router(users.router)
    app.include_router(movies.router)

    return app
