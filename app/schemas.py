from datetime import date

from pydantic import BaseModel


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

    class Config:
        orm_mode = True
