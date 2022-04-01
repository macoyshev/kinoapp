from typing import Optional

from fastapi import APIRouter, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from app.api import schemas
from app.api.services import SecurityService, UserService

router = APIRouter(
    prefix='/users',
    tags=['users'],
)

security = HTTPBasic()


@router.get('/', response_model=list[schemas.User])
def fetch_users(
    offset: Optional[int] = None,
    limit: Optional[int] = None,
    credentials: HTTPBasicCredentials = Depends(security),
) -> list[schemas.User]:
    SecurityService.authenticate_user(credentials)

    users = UserService.get_all(offset=offset, limit=limit)

    return [schemas.User.from_orm(user) for user in users]


@router.post('/', response_model=schemas.User)
def create_user(user: schemas.UserCreate) -> schemas.User:
    user = UserService.create(user)

    return schemas.User.from_orm(user)
