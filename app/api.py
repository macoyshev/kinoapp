from typing import Optional

from fastapi import Depends, FastAPI
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from app import schemas
from app.database import create_bd
from app.services import MovieService, ReviewService, SecurityService, UserService

api = FastAPI()

security = HTTPBasic()

create_bd()


@api.get('/users', response_model=list[schemas.User])
def fetch_users(
    credentials: HTTPBasicCredentials = Depends(security),
) -> list[schemas.User]:
    SecurityService.authenticate_user(credentials)

    users = UserService.get_all()

    return [schemas.User.from_orm(user) for user in users]


@api.post('/users', response_model=schemas.User)
def create_user(user: schemas.UserCreate) -> schemas.User:
    user = UserService.create(user)

    return schemas.User.from_orm(user)


@api.get('/movies', response_model=list[schemas.Movie])
def fetch_movies(
    year: Optional[int] = None,
    substr: Optional[str] = None,
    credentials: HTTPBasicCredentials = Depends(security),
) -> list[schemas.Movie]:
    SecurityService.authenticate_user(credentials)

    movies = MovieService.get_all(year=year, substr=substr)

    return [schemas.Movie.from_orm(movie) for movie in movies]


@api.post('/movies', response_model=schemas.Movie)
def create_movie(
    movie: schemas.MovieCreate, credentials: HTTPBasicCredentials = Depends(security)
) -> schemas.Movie:
    SecurityService.authenticate_user(credentials)

    movie = MovieService.create(movie)

    return schemas.Movie.from_orm(movie)


@api.post('/movies/{movie_id}/reviews', response_model=schemas.Review)
def create_movie_review(
    movie_id: int,
    review: schemas.ReviewCreate,
    credentials: HTTPBasicCredentials = Depends(security),
) -> schemas.Review:
    SecurityService.authenticate_user(credentials)

    user = UserService.find_by_name(credentials.username)

    review = ReviewService.create(review=review, movie_id=movie_id, user_id=user.id)

    return schemas.Review.from_orm(review)


@api.get('/movies/{movie_id}/reviews', response_model=list[schemas.Review])
def get_movie_reviews(
    movie_id: int,
    credentials: HTTPBasicCredentials = Depends(security),
) -> list[schemas.Review]:
    SecurityService.authenticate_user(credentials)

    reviews = ReviewService.get_by_movie_id(movie_id)

    return [schemas.Review.from_orm(rev) for rev in reviews]
