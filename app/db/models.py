from datetime import datetime

from sqlalchemy import Column, Date, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)
    password = Column(String)
    salt = Column(String)

    reviews = relationship(
        'Review', uselist=True, lazy='subquery', back_populates='user'
    )

    def __repr__(self) -> str:
        return f'user: id={self.id}, name={self.name}'


class Movie(Base):
    __tablename__ = 'movies'

    id = Column(Integer, primary_key=True)
    title = Column(String(50), unique=True, nullable=False)
    realise_date = Column(Date, default=datetime.utcnow().date())
    ratings_avg = Column(String(4), default='0.0')
    ratings_sum = Column(Integer, default=0)
    ratings_count = Column(Integer, default=0)
    comments_count = Column(Integer, default=0)

    reviews = relationship(
        'Review', uselist=True, lazy='subquery', back_populates='movie'
    )

    def __repr__(self) -> str:
        return f'movie: id={self.id}, title={self.title}, avg-rating={self.ratings_avg}'


class Review(Base):
    __tablename__ = 'reviews'

    id = Column(Integer, primary_key=True)
    rating = Column(Integer, nullable=False)
    comment = Column(String, nullable=False)
    movie_id = Column(Integer, ForeignKey(Movie.id))
    user_id = Column(Integer, ForeignKey(User.id))

    user = relationship(User, lazy='subquery', uselist=False, back_populates='reviews')
    movie = relationship(
        Movie, lazy='subquery', uselist=False, back_populates='reviews'
    )

    def __repr__(self) -> str:
        return (
            f'review: id={self.id}, user-id={self.user_id}, '
            f'movie-id={self.movie_id}, rating={self.rating}, comment={self.comment}'
        )
