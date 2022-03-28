import pytest
from fastapi.security import HTTPBasicCredentials

from app import schemas
from app.exceptions import InvalidCredentials, UserAlreadyExists
from app.services import SecurityService, UserService


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
    with pytest.raises(UserAlreadyExists):
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
