import random
import secrets
import string
from hashlib import pbkdf2_hmac
from typing import Optional

from fastapi.security import HTTPBasicCredentials
from loguru import logger
from sqlalchemy import desc, sql

from app import models, schemas
from app.database import create_session
from app.exceptions import InvalidCredentials, ResourceAlreadyExists


class UserService:
    @staticmethod
    def get_all(
        offset: Optional[int] = None, limit: Optional[int] = None
    ) -> list[models.User]:
        """
        :param offset: number of skipped elements
        :param limit: max number of returned elements
        :return: list of users
        """

        with create_session(expire_on_commit=False) as session:
            users = session.query(models.User)

            if limit is not None:
                users = users.limit(limit)

            if offset is not None:
                users = users.offset(offset)

            users = users.all()

        return users

    @staticmethod
    def find_by_id(user_id: int) -> models.User:
        """
        :param user_id: id of user
        :return: user entity
        """

        with create_session(expire_on_commit=False) as session:
            user = session.query(models.User).filter(models.User.id == user_id).first()

        return user

    @staticmethod
    def find_by_name(name: str) -> models.User:
        """
        :param name: name of user
        :return: user entity
        """

        with create_session(expire_on_commit=False) as session:
            user = session.query(models.User).filter(models.User.name == name).first()

        return user

    @staticmethod
    def create(user: schemas.UserCreate) -> models.User:
        """
        Creates a new user. Password is hashed with 'salt' adding

        :param user: schema of userCreate
        :return: user entity
        :raises ResourceAlreadyExists: if user already exists
        """

        if UserService.find_by_name(user.name):
            raise ResourceAlreadyExists(entity='user')

        salt = SecurityService.generate_random_string()
        hashed_password = SecurityService.hash_password(user.password, salt)

        with create_session(expire_on_commit=False) as session:
            user = models.User(name=user.name, password=hashed_password, salt=salt)

            session.add(user)

        logger.info(f'{user} was created')

        return user


class MovieService:
    @staticmethod
    def get_all(
        top: Optional[int] = None,
        substr: Optional[str] = None,
        year: Optional[int] = None,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
    ) -> list[models.Movie]:
        """
        :param top: filter by average rating, filter all movies with rating more t
        :param substr: filter by substring in title
        :param year: filter by year of realise
        :param offset: number of skipped elements
        :param limit: max number of returned elements
        :return: list of movies
        """

        with create_session(expire_on_commit=False) as session:
            movies = session.query(models.Movie)
            if year:
                movies = movies.filter(
                    sql.extract('year', models.Movie.realise_date) == year
                )
            if substr:
                movies = movies.filter(models.Movie.title.contains(substr))

            if top:
                movies = movies.order_by(desc(models.Movie.ratings_avg)).limit(top)

            if limit is not None:
                movies = movies.limit(limit)

            if offset is not None:
                movies = movies.offset(offset)

            movies = movies.all()

        return movies

    @staticmethod
    def create(movie: schemas.MovieCreate) -> models.Movie:
        """
        :param movie: entity of MovieCreate schema
        :return: created movie
        """

        if MovieService.find_by_title(movie.title):
            raise ResourceAlreadyExists(entity='movie')

        with create_session(expire_on_commit=False) as session:
            movie = models.Movie(title=movie.title)
            session.add(movie)

        logger.info(f'{movie} was created')
        return movie

    @staticmethod
    def find_by_title(title: str) -> Optional[models.Movie]:
        """
        :param title: title of searching movie
        :return: movie
        """

        with create_session(expire_on_commit=False) as session:
            movie = (
                session.query(models.Movie).filter(models.Movie.title == title).first()
            )

        return movie

    @staticmethod
    def find_by_id(movie_id: int) -> Optional[models.Movie]:
        """
        :param movie_id: id of searching movie
        :return: movie
        """

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
        """
        Creates a review on the specified movie. Also, this function updates some movie parameters:
        count of ratings, count of comments, the sum of all ratings, and the average rating

        :param review: entity of ReviewCreate schema
        :param movie_id: id of the movie being reviewed
        :param user_id: id of reviewer
        :return: created review
        :raises ResourceAlreadyExists: if the movie has already been reviewed by a user.
        """

        if ReviewService.movie_reviewed_by_user(movie_id=movie_id, user_id=user_id):
            raise ResourceAlreadyExists(entity='review')

        with create_session(expire_on_commit=False) as session:
            review = models.Review(
                rating=review.rating,
                movie_id=movie_id,
                user_id=user_id,
                comment=review.comment,
            )
            session.add(review)

            # change movie comments and rating count
            movie = (
                session.query(models.Movie).filter(models.Movie.id == movie_id).first()
            )
            movie.ratings_sum += review.rating
            movie.comments_count += 1
            movie.ratings_count += 1
            movie.ratings_avg = str(round(movie.ratings_sum / movie.ratings_count, 1))

        logger.info(f'{review} was created')
        return review

    @staticmethod
    def get_by_movie_id(
        movie_id: int, offset: Optional[int] = None, limit: Optional[int] = None
    ) -> list[models.Movie]:
        """
        :param offset: number of skipped elements
        :param limit: max number of returned elements
        :param movie_id: id of the movie
        :return: list of reviews on the specified movie
        """
        with create_session(expire_on_commit=False) as session:
            reviews = session.query(models.Review).filter(
                models.Review.movie_id == movie_id
            )

            if limit is not None:
                reviews = reviews.limit(limit)

            if offset is not None:
                reviews = reviews.offset(offset)

            reviews = reviews.all()

        return reviews

    @staticmethod
    def movie_reviewed_by_user(movie_id: int, user_id: int) -> bool:
        user = UserService.find_by_id(user_id)

        for rev in user.reviews:
            if rev.movie_id == movie_id:
                return True
        return False


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
