from typing import Optional

from fastapi.exceptions import HTTPException


class ResourceAlreadyExists(HTTPException):
    """
    Raises in case of attempt to create an already existing entity
    """

    def __init__(self, entity: Optional[str] = 'Resource') -> None:
        super().__init__(status_code=409, detail=f'{entity} already exists')


class InvalidCredentials(HTTPException):
    """
    Raises in case of invalid credentials
    """

    def __init__(self) -> None:
        super().__init__(status_code=401, detail='Invalid password or name')
