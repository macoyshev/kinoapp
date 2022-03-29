import pytest
from fastapi.security import HTTPBasicCredentials
from pydantic import ValidationError

from app import schemas
from app.exceptions import InvalidCredentials, ResourceAlreadyExists
from app.services import MovieService, ReviewService, SecurityService, UserService


def test_get_all_users(test_user):
    user_test = test_user
    users = UserService.get_all()
    assert len(users) == 1
    assert users[0].name == user_test.name


def generate_random_string():
    salt = SecurityService.generate_random_string()

    assert len(salt) == 10


def test_validate_password(test_user):
    assert SecurityService.validate_password(
        hashed_password=test_user.password,
        password=test_user.password_not_hashed,
        salt=test_user.salt,
    )


def test_create_user_exception(test_user):
    with pytest.raises(ResourceAlreadyExists):
        user = schemas.UserCreate(
            name=test_user.name, password=test_user.password_not_hashed
        )
        UserService.create(user)


def test_authenticate_invalid_user(test_user):
    with pytest.raises(InvalidCredentials):
        SecurityService.authenticate_user(
            credentials=HTTPBasicCredentials(
                username=test_user.name, password=test_user.password
            )
        )


def test_movie_get_all(test_movie):
    movies = MovieService.get_all()

    assert len(movies) == 1
    assert movies[0].title == test_movie.title


def test_create_existing_movie(test_movie):
    with pytest.raises(ResourceAlreadyExists):
        MovieService.create(schemas.MovieCreate(title=test_movie.title))


def test_find_movie_by_title(test_movie):
    movie = MovieService.find_by_title(test_movie.title)

    assert movie
    assert movie.title == test_movie.title


def test_find_movie_by_id(test_movie):
    movie = MovieService.find_by_id(test_movie.id)

    assert movie
    assert movie.id == test_movie.id


def test_movie_params(test_review):
    movie = MovieService.find_by_id(test_review.movie_id)

    assert movie
    assert movie.ratings_avg == '5.0'
    assert movie.comments_count == 1
    assert movie.ratings_count == 1


def test_create_existing_review(test_review):
    with pytest.raises(ResourceAlreadyExists):
        ReviewService.create(
            schemas.ReviewCreate(rating=5, comment='ok'),
            test_review.movie_id,
            test_review.user_id,
        )


def test_find_review_by_user_id(test_review):
    review = ReviewService.find_by_user_id(test_review.user_id)

    assert review
    assert review.user_id == test_review.user_id


def test_get_by_movie_id(test_review):
    reviews = ReviewService.get_by_movie_id(test_review.movie_id)

    assert len(reviews) == 1
    assert reviews[0].id == test_review.id


def test_invalid_rating_for_review(test_user, test_movie):
    with pytest.raises(ValidationError):
        ReviewService.create(
            schemas.ReviewCreate(rating=11, comment='ok'), test_movie.id, test_user.id
        )
