import pytest
from fastapi.security import HTTPBasicCredentials
from pydantic import ValidationError

from app.api import schemas
from app.api.exceptions import InvalidCredentials, ResourceAlreadyExists
from app.api.services import MovieService, ReviewService, SecurityService, UserService


def test_get_all_users():
    UserService.create(schemas.UserCreate(name='test1', password='test1'))
    UserService.create(schemas.UserCreate(name='test2', password='test2'))
    UserService.create(schemas.UserCreate(name='test3', password='test3'))

    users = UserService.get_all(offset=1, limit=2)

    assert len(users) == 2


def generate_random_string():
    salt = SecurityService.generate_random_string()

    assert len(salt) == 10


def test_create_user_exception(test_user):
    with pytest.raises(ResourceAlreadyExists):
        user = schemas.UserCreate(
            name=test_user.name, password=test_user.password_not_hashed
        )
        UserService.create(user)


def test_movie_reviewed_by_user(test_review):
    assert ReviewService.movie_reviewed_by_user(
        test_review.movie_id, test_review.user_id
    )


def test_validate_password(test_user):
    assert SecurityService.validate_password(
        hashed_password=test_user.password,
        password=test_user.password_not_hashed,
        salt=test_user.salt,
    )


def test_movie_not_reviewed_by_user(test_movie, test_user):
    assert not ReviewService.movie_reviewed_by_user(test_movie.id, test_user.id)


def test_authenticate_invalid_user(test_user):
    with pytest.raises(InvalidCredentials):
        SecurityService.authenticate_user(
            credentials=HTTPBasicCredentials(
                username=test_user.name, password=test_user.password
            )
        )


def test_movie_get_all(test_movie):
    movies = MovieService.get_all(offset=0, limit=1)

    assert len(movies) == 1
    assert movies[0].title == test_movie.title


@pytest.mark.usefixtures('test_movie')
@pytest.mark.parametrize('year, expected_len', [(2022, 1), (2024, 0), (2000, 0)])
def test_movie_get_all_with_year_filter(year, expected_len):
    movies = MovieService.get_all(year=year)

    assert len(movies) == expected_len


@pytest.mark.usefixtures('test_movie')
@pytest.mark.parametrize('substr, expected_len', [('test', 1), ('te', 1), ('wrong', 0)])
def test_movie_get_all_with_substr_filter(substr, expected_len):
    movies = MovieService.get_all(substr=substr)

    assert len(movies) == expected_len


@pytest.mark.usefixtures('test_movie')
@pytest.mark.parametrize(
    'page, page_size, expected_len', [(0, 1, 1), (1, 10, 0), (2, 2, 0)]
)
def test_movie_get_all_with_pagesize_page_filter(page, page_size, expected_len):
    movies = MovieService.get_all(offset=page, limit=page_size)

    assert len(movies) == expected_len


def test_create_existing_movie(test_movie):
    with pytest.raises(ResourceAlreadyExists):
        MovieService.create(schemas.MovieCreate(title=test_movie.title))


def test_find_movie_by_title(test_movie):
    movie = MovieService.find_by_title(test_movie.title)

    assert movie
    assert movie.title == test_movie.title


def test_find_movie_by_id(test_movie):
    movie = MovieService.find_by_id(test_movie.id)

    assert movie
    assert movie.id == test_movie.id


def test_movie_params(test_review):
    movie = MovieService.find_by_id(test_review.movie_id)

    assert movie
    assert movie.ratings_avg == '5.0'
    assert movie.comments_count == 1
    assert movie.ratings_count == 1


def test_create_existing_review(test_review):
    with pytest.raises(ResourceAlreadyExists):
        ReviewService.create(
            schemas.ReviewCreate(rating=5, comment='ok'),
            test_review.movie_id,
            test_review.user_id,
        )


def test_get_by_movie_id(test_review):
    test_movie2 = MovieService.create(schemas.MovieCreate(title='test2'))
    ReviewService.create(
        schemas.ReviewCreate(rating=1, comment='ok'),
        user_id=test_review.user_id,
        movie_id=test_movie2.id,
    )
    reviews = ReviewService.get_by_movie_id(test_review.movie_id, offset=0, limit=1)

    assert len(reviews) == 1
    assert reviews[0].id == test_review.id


def test_invalid_rating_for_review(test_user, test_movie):
    with pytest.raises(ValidationError):
        ReviewService.create(
            schemas.ReviewCreate(rating=11, comment='ok'), test_movie.id, test_user.id
        )


def test_get_top_movies(test_user, test_movie):
    test_movie2 = MovieService.create(schemas.MovieCreate(title='test2'))

    ReviewService.create(
        schemas.ReviewCreate(rating=10, comment='ok'),
        user_id=test_user.id,
        movie_id=test_movie2.id,
    )

    movies = MovieService.get_all(top=2)

    assert movies
    assert len(movies) == 2
    assert movies[0].title == test_movie2.title
    assert movies[1].title == test_movie.title


@pytest.mark.parametrize('limit, expected', [(1, 1), (2, 2), (3, 3)])
def test_get_all_movies_limit(limit, expected):
    MovieService.create(schemas.MovieCreate(title='test_1'))
    MovieService.create(schemas.MovieCreate(title='test_2'))
    MovieService.create(schemas.MovieCreate(title='test_3'))

    movies = MovieService.get_all(limit=limit)

    assert len(movies) == expected
