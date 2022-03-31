from typing import Optional

from fastapi import APIRouter, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from app.api import schemas
from app.api.services import SecurityService, MovieService, UserService, ReviewService

router = APIRouter(
    prefix="/movies",
    tags=["movies"],
)

security = HTTPBasic()


@router.get('/', response_model=list[schemas.Movie])
def fetch_movies(
    # pylint: disable=too-many-arguments
    # task requires 5 filters
    top: Optional[int] = None,
    substr: Optional[str] = None,
    year: Optional[int] = None,
    offset: Optional[int] = None,
    limit: Optional[int] = None,
    credentials: HTTPBasicCredentials = Depends(security),
) -> list[schemas.Movie]:
    SecurityService.authenticate_user(credentials)

    movies = MovieService.get_all(
        year=year, substr=substr, offset=offset, limit=limit, top=top
    )

    return [schemas.Movie.from_orm(movie) for movie in movies]


@router.post('/', response_model=schemas.Movie)
def create_movie(
    movie: schemas.MovieCreate, credentials: HTTPBasicCredentials = Depends(security)
) -> schemas.Movie:
    SecurityService.authenticate_user(credentials)

    movie = MovieService.create(movie)

    return schemas.Movie.from_orm(movie)


@router.post('/{movie_id}/reviews', response_model=schemas.Review)
def create_movie_review(
    movie_id: int,
    review: schemas.ReviewCreate,
    credentials: HTTPBasicCredentials = Depends(security),
) -> schemas.Review:
    SecurityService.authenticate_user(credentials)

    user = UserService.find_by_name(credentials.username)

    review = ReviewService.create(review=review, movie_id=movie_id, user_id=user.id)

    return schemas.Review.from_orm(review)


@router.get('/{movie_id}/reviews', response_model=list[schemas.Review])
def get_movie_reviews(
    movie_id: int,
    offset: Optional[int] = None,
    limit: Optional[int] = None,
    credentials: HTTPBasicCredentials = Depends(security),
) -> list[schemas.Review]:
    SecurityService.authenticate_user(credentials)

    reviews = ReviewService.get_by_movie_id(
        movie_id=movie_id, offset=offset, limit=limit
    )

    return [schemas.Review.from_orm(rev) for rev in reviews]
