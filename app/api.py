from fastapi import Depends, FastAPI
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from app import schemas
from app.database import create_bd
from app.services import MovieService, ReviewService, SecurityService, UserService

api = FastAPI()

security = HTTPBasic()

create_bd()


@api.get('/users')
def fetch_users(
    credentials: HTTPBasicCredentials = Depends(security),
) -> list[schemas.User]:
    SecurityService.authenticate_user(credentials)

    users = UserService.get_all()

    return [schemas.User.from_orm(user) for user in users]


@api.post('/users')
def create_user(user: schemas.UserCreate) -> schemas.User:
    user = UserService.create(user)

    return schemas.User.from_orm(user)


@api.get('/movies')
def fetch_movies(
    credentials: HTTPBasicCredentials = Depends(security),
) -> list[schemas.Movie]:
    SecurityService.authenticate_user(credentials)

    movies = MovieService.get_all()

    return [schemas.Movie.from_orm(movie) for movie in movies]


@api.post('/movies')
def create_movie(
    movie: schemas.MovieCreate, credentials: HTTPBasicCredentials = Depends(security)
) -> schemas.Movie:
    SecurityService.authenticate_user(credentials)

    movie = MovieService.create(movie)

    return schemas.Movie.from_orm(movie)


@api.post('/movies/{movie_id}/reviews')
def create_movie_review(
    movie_id: int,
    review: schemas.ReviewCreate,
    credentials: HTTPBasicCredentials = Depends(security),
):
    SecurityService.authenticate_user(credentials)

    user = UserService.find_by_name(credentials.username)

    ReviewService.create_review(review=review, movie_id=movie_id, user_id=user.id)
