from functools import wraps
from typing import Any, Callable

from fastapi.security import HTTPBasic

from app.exceptions import BadCredentials, InvalidCredentials
from app.services import SecurityService, UserService

security = HTTPBasic()


def auth(func: Callable[..., Any]) -> Callable[..., Any]:
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any):
        credentials = kwargs['credentials']
        user = UserService.find_by_name(credentials.username)

        print(user)

        if not user or not SecurityService.validate_password(
            password=credentials.password,
            hashed_password=user.password,
            salt=user.salt,
        ):
            raise InvalidCredentials()

        func(*args, **kwargs)

    return wrapper

