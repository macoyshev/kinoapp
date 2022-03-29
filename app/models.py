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

    def __repr__(self) -> str:
        return f'User(id:{self.id}, name:{self.name}'


class Movie(Base):
    __tablename__ = 'movies'

    id = Column(Integer, primary_key=True)
    title = Column(String(50), unique=True, nullable=False)
    realise_date = Column(Date, default=datetime.utcnow().date())
    ratings_avg = Column(Integer, default=0)
    ratings_counts = Column(Integer, default=0)
    comments_count = Column(Integer, default=0)

    reviews = relationship('Review', uselist=True, lazy='subquery')

    def __repr__(self) -> str:
        return f'Movie(id:{self.id}, title:{self.title}'


class Review(Base):
    __tablename__ = 'reviews'

    id = Column(Integer, primary_key=True)
    rating = Column(Integer, nullable=False)
    comment = Column(String, nullable=False)
    movie_id = Column(Integer, ForeignKey(Movie.id))
    user_id = Column(Integer, ForeignKey(User.id))

    def __repr__(self) -> str:
        return f'Review(id:{self.id}, user_id:{self.user_id}, movie_id:{self.movie_id})'
