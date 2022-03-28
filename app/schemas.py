from datetime import date

from pydantic import BaseModel, constr, validator


class ReviewBase(BaseModel):
    rating: int
    comment: constr(min_length=1)

    @validator('rating')
    def range_rating(cls, v):
        if v < 0 or v > 10:
            raise ValueError('rating must be from 0 to 10')
        return v


class Review(ReviewBase):
    id: int

    class Config:
        orm_mode = True


class ReviewCreate(ReviewBase):
    pass


class UserBase(BaseModel):
    name: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int

    class Config:
        orm_mode = True


class MovieBase(BaseModel):
    title: str


class MovieCreate(MovieBase):
    pass


class Movie(MovieBase):
    id: int
    realise_date: date
    ratings_avg: int
    ratings_counts: int
    comments_count: int
    reviews: list[Review]

    class Config:
        orm_mode = True
