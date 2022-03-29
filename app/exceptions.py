from typing import Optional

from fastapi.exceptions import HTTPException


class ResourceAlreadyExists(HTTPException):
    def __init__(self, entity: Optional[str] = 'Resource') -> None:
        super().__init__(status_code=409, detail=f'{entity} already exists')


class InvalidCredentials(HTTPException):
    def __init__(self) -> None:
        super().__init__(status_code=401, detail='Invalid credentials')
