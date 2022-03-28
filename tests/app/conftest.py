from base64 import b64encode

import pytest
from fastapi.testclient import TestClient

from app import schemas
from app.api import api
from app.database import clear_db, create_bd
from app.services import UserService


@pytest.fixture(autouse=True)
def _init_db():
    create_bd(mode='TESTING')

    yield

    clear_db(mode='TESTING')


@pytest.fixture
def client():
    _client = TestClient(api)

    yield _client


@pytest.fixture
def test_user():
    _test_user = UserService.create(schemas.UserCreate(name='test', password='test'))

    _test_user.base64 = b64encode('test:test'.encode('utf-8')).decode('utf-8')
    _test_user.base64_invalid_username = (
        b64encode('wrong:test'.encode('utf-8')).decode('utf-8'),
    )
    _test_user.base64_invalid_password = (
        b64encode('test:wrong'.encode('utf-8')).decode('utf-8'),
    )
    _test_user.password_not_hashed = 'test'

    return _test_user
