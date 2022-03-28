from fastapi import FastAPI, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from app import schemas
from app.database import create_bd
from app.services import MovieService, UserService
from app.utils import auth

api = FastAPI()
security = HTTPBasic()
create_bd()


# @api.get('/users')
# def fetch_users(
#     credentials: HTTPBasicCredentials = Depends(security),
# ) -> list[schemas.User]:
#     user = UserService.find_by_name(credentials.username)
#
#     if not user:
#         raise BadCredentials()
#
#     if not SecurityService.validate_password(
#         password=credentials.password, hashed_password=user.password, salt=user.salt
#     ):
#         raise InvalidPassword()
#
#     users = UserService.get_all()
#
#     return [schemas.User.from_orm(user) for user in users]
#
#
@api.post('/users')
def create_user(user: schemas.UserCreate) -> schemas.User:
    user = UserService.create(user)

    return schemas.User.from_orm(user)


@api.get('/movies')
@auth
def fetch_movies(credentials: HTTPBasicCredentials = Depends(security)):
    movies = MovieService.get_all()

    return [schemas.Movie.from_orm(movie) for movie in movies]


@api.post('/movies')
def create_movie(movie: schemas.MovieCreate):
    movie = MovieService.create(movie)

    return schemas.Movie.from_orm(movie)
