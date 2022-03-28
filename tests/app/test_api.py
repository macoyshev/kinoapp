from http import HTTPStatus

import pytest

from app.exceptions import BadCredentials, InvalidCredentials


def test_no_credentials(client):
    res = client.get('/users')

    assert res.status_code == HTTPStatus.UNAUTHORIZED


def test_invalid_password(client, test_user):
    with pytest.raises(InvalidCredentials):
        client.get(
            '/users',
            headers={'Authorization': f'Basic {test_user.base64_invalid_password}'},
        )


def test_bad_credentials(client, test_user):
    with pytest.raises(BadCredentials):
        client.get(
            '/users',
            headers={'Authorization': f'Basic {test_user.base64_invalid_username}'},
        )


def test_create_user(client):
    res = client.post('/users', json={'name': 'max', 'password': 2303})
    user = res.json()

    assert res.status_code == 200
    assert user.get('name') == 'max'
    assert user.get('id') == 1


def test_fetch_users(client, test_user):
    res = client.get('/users', headers={'Authorization': f'Basic {test_user.base64}'})
    user = res.json()[0]

    assert res.status_code == 200
    assert user.get('name') == test_user.name
