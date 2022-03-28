import random
import secrets
import string
from hashlib import pbkdf2_hmac

from app import models, schemas
from app.database import create_session
from app.exceptions import UserAlreadyExists


class UserService:
    @staticmethod
    def get_all() -> list[models.User]:
        with create_session(expire_on_commit=False) as session:
            users = session.query(models.User).all()

        return users

    @staticmethod
    def find_by_name(name: str) -> models.User:
        with create_session(expire_on_commit=False) as session:
            user = session.query(models.User).filter(models.User.name == name).first()

        return user

    @staticmethod
    def create(user: schemas.UserCreate) -> models.User:
        if UserService.find_by_name(user.name):
            raise UserAlreadyExists()

        salt = SecurityService.generate_random_string()
        hashed_password = SecurityService.hash_password(user.password, salt)

        with create_session(expire_on_commit=False) as session:
            user = models.User(name=user.name, password=hashed_password, salt=salt)

            session.add(user)

        return user


class SecurityService:
    @staticmethod
    def hash_password(password: str, salt: str) -> str:
        hashed_password = pbkdf2_hmac('sha256', password.encode(), salt.encode(), 10)

        return hashed_password.hex()

    @staticmethod
    def validate_password(password: str, hashed_password: str, salt: str) -> bool:
        password_to_verify = SecurityService.hash_password(password, salt)

        return secrets.compare_digest(hashed_password, password_to_verify)

    @staticmethod
    def generate_random_string(length: int = 10) -> str:
        return ''.join(random.choice(string.ascii_letters) for _ in range(length))


class MovieService:
    @staticmethod
    def get_all():
        with create_session(expire_on_commit=False) as session:
            movies = session.query(models.Movie).all()

        return movies

    @staticmethod
    def create(movie: schemas.MovieCreate):
        with create_session(expire_on_commit=False) as session:
            movie = models.Movie(title=movie.title)
            session.add(movie)

        return movie
