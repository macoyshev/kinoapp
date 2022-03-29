from base64 import b64encode

import pytest
from fastapi.testclient import TestClient

from app import schemas
from app.api import api
from app.database import clear_db, create_bd
from app.services import MovieService, ReviewService, UserService


@pytest.fixture(autouse=True)
def _init_db():
    create_bd(mode='TESTING')

    yield

    clear_db(mode='TESTING')


@pytest.fixture
def client():
    _client = TestClient(api)

    yield _client


@pytest.fixture(name='test_user')
def create_test_user():
    user = UserService.create(schemas.UserCreate(name='test', password='test'))

    user.base64 = b64encode('test:test'.encode('utf-8')).decode('utf-8')
    user.base64_invalid_username = (
        b64encode('wrong:test'.encode('utf-8')).decode('utf-8'),
    )
    user.base64_invalid_password = (
        b64encode('test:wrong'.encode('utf-8')).decode('utf-8'),
    )
    user.password_not_hashed = 'test'

    return user


@pytest.fixture(name='test_movie')
def create_test_movie():
    movie = MovieService.create(schemas.MovieCreate(title='test_movie'))

    return movie


@pytest.fixture(name='test_review')
def create_test_review(test_movie, test_user):
    review = ReviewService.create(
        schemas.ReviewCreate(rating=5, comment='ok'),
        movie_id=test_movie.id,
        user_id=test_user.id,
    )

    return review
