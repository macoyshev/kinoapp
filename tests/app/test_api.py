from http import HTTPStatus


def test_no_credentials(client):
    res = client.get('/users')

    assert res.status_code == HTTPStatus.UNAUTHORIZED


def test_invalid_password(client):
    res = client.get(
        '/users',
        headers={'Authorization': 'Basic invalid:data'},
    )

    assert res.status_code == 401


def test_fetch_users(client, test_user):
    res = client.get('/users', headers={'Authorization': f'Basic {test_user.base64}'})
    user = res.json()[0]

    assert res.status_code == 200
    assert user.get('name') == test_user.name


def test_create_user(client):
    res = client.post('/users/', json={'name': 'test', 'password': 'test'})
    user = res.json()

    assert res.status_code == 200
    assert user.get('name') == 'test'
    assert user.get('password') is None


def test_fetch_movies(client, test_user, test_movie):
    res = client.get('/movies', headers={'Authorization': f'Basic {test_user.base64}'})

    movies = res.json()
    assert len(movies) == 1
    assert movies[0].get('title') == test_movie.title


def test_create_movie(client, test_user):
    res = client.post(
        '/movies/',
        json={'title': 'test'},
        headers={'Authorization': f'Basic {test_user.base64}'},
    )
    movie = res.json()

    assert res.status_code == 200
    assert movie.get('title') == 'test'


def test_create_movie_review(client, test_movie, test_user):
    res = client.post(
        f'/movies/{test_movie.id}/reviews',
        json={'rating': 10, 'comment': 'top'},
        headers={'Authorization': f'Basic {test_user.base64}'},
    )

    rev = res.json()
    assert rev.get('user_id') == test_user.id
    assert rev.get('rating') == 10
    assert rev.get('comment') == 'top'
    assert rev.get('movie_id') == test_movie.id


def test_get_movie_reviews(client, test_review, test_user):
    res = client.get(
        f'/movies/{test_review.movie_id}/reviews',
        headers={'Authorization': f'Basic {test_user.base64}'},
    )

    revs = res.json()

    assert revs[0].get('id') == test_review.id
    assert revs[0].get('user_id') == test_user.id
    assert revs[0].get('rating') == test_review.rating
    assert revs[0].get('comment') == test_review.comment
    assert revs[0].get('movie_id') == test_review.movie_id
