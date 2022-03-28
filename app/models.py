from datetime import datetime

from sqlalchemy import Column, Date, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)
    password = Column(String)
    salt = Column(String)

    reviews = relationship('Review', uselist=True, lazy='subquery')


class Movie(Base):
    __tablename__ = 'movies'

    id = Column(Integer, primary_key=True)
    title = Column(String(50), unique=True, nullable=False)
    realise_date = Column(Date, default=datetime.utcnow().date())
    ratings_avg = Column(Integer, default=0)
    ratings_counts = Column(Integer, default=0)
    comments_count = Column(Integer, default=0)

    reviews = relationship('Review', uselist=True, lazy='subquery')


class Review(Base):
    __tablename__ = 'reviews'

    id = Column(Integer, primary_key=True)
    rating = Column(Integer, nullable=False)
    comment = Column(String, nullable=True, unique=False)
    movie_id = Column(Integer, ForeignKey(Movie.id))
    user_id = Column(Integer, ForeignKey(User.id))
