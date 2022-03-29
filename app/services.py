import random
import secrets
import string
from hashlib import pbkdf2_hmac
from typing import Optional

from fastapi.security import HTTPBasicCredentials
from loguru import logger

from app import models, schemas
from app.database import create_session
from app.exceptions import InvalidCredentials, ResourceAlreadyExists


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
            raise ResourceAlreadyExists(entity='user')

        salt = SecurityService.generate_random_string()
        hashed_password = SecurityService.hash_password(user.password, salt)

        with create_session(expire_on_commit=False) as session:
            user = models.User(name=user.name, password=hashed_password, salt=salt)

            session.add(user)

        logger.info(f'{user} was created')
        return user


class SecurityService:
    @staticmethod
    def authenticate_user(credentials: HTTPBasicCredentials) -> None:
        user = UserService.find_by_name(credentials.username)

        if not user or not SecurityService.validate_password(
            hashed_password=user.password, password=credentials.password, salt=user.salt
        ):
            raise InvalidCredentials()

        logger.info(f'{user} passed authentication')

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
    def get_all() -> list[models.Movie]:
        with create_session(expire_on_commit=False) as session:
            movies = session.query(models.Movie).all()

        return movies

    @staticmethod
    def create(movie: schemas.MovieCreate) -> models.Movie:
        if MovieService.find_by_title(movie.title):
            raise ResourceAlreadyExists(entity='movie')

        with create_session(expire_on_commit=False) as session:
            movie = models.Movie(title=movie.title)
            session.add(movie)

        logger.info(f'{movie} was created')
        return movie

    @staticmethod
    def find_by_title(title: str) -> Optional[models.Movie]:
        with create_session(expire_on_commit=False) as session:
            movie = (
                session.query(models.Movie).filter(models.Movie.title == title).first()
            )

        return movie

    @staticmethod
    def find_by_id(movie_id: int) -> Optional[models.Movie]:
        with create_session(expire_on_commit=False) as session:
            movie = (
                session.query(models.Movie).filter(models.Movie.id == movie_id).first()
            )

        return movie


class ReviewService:
    @staticmethod
    def create(
        review: schemas.ReviewCreate, movie_id: int, user_id: int
    ) -> models.Review:
        if ReviewService.find_by_user_id(user_id):
            raise ResourceAlreadyExists(entity='review')

        with create_session(expire_on_commit=False) as session:
            rev = models.Review(
                rating=review.rating,
                movie_id=movie_id,
                user_id=user_id,
                comment=review.comment,
            )
            session.add(rev)

            # change movie comments and rating count
            movie = (
                session.query(models.Movie).filter(models.Movie.id == movie_id).first()
            )
            movie.ratings_sum += review.rating
            movie.comments_count += 1
            movie.ratings_count += 1
            movie.ratings_avg = str(round(movie.ratings_sum / movie.ratings_count, 1))

        logger.info(f'{rev} was created')
        return rev

    @staticmethod
    def get_by_movie_id(movie_id: int) -> list[models.Movie]:
        with create_session(expire_on_commit=False) as session:
            revs = session.query(models.Review).filter(
                models.Review.movie_id == movie_id
            )

        return list(revs)

    @staticmethod
    def find_by_user_id(user_id: int) -> Optional[models.Review]:
        with create_session(expire_on_commit=False) as session:
            rev = (
                session.query(models.Review)
                .filter(models.Review.user_id == user_id)
                .first()
            )

        return rev
