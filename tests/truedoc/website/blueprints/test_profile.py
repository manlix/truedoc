from http import HTTPStatus

import pytest
import requests


@pytest.fixture()
def endpoint():
    return 'http://truedoc-app.localhost/profile/'


def test_create_and_delete_profile(endpoint):
    """Create and delete profile."""
    payload = dict(
        email='test@example.com',
        password='password',
    )

    response = requests.post(endpoint, json=payload)

    assert response.status_code == HTTPStatus.OK  # Profile created (200)

    profile_id = response.json()['result']['profile_id']

    response = requests.delete(f'{endpoint}{profile_id}')

    assert response.status_code == HTTPStatus.OK  # Profile deleted (200)


def test_create_profile_bad_request(endpoint):
    """Create profile: 400 — Bad request."""
    headers = {
        'Content-type': 'application/json'
    }

    response = requests.post(endpoint, headers=headers)

    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_create_profile_not_acceptable(endpoint):
    """Create profile: 406 — Not Acceptable."""
    payload = dict(
        email='test@example.com',
    )

    response = requests.post(endpoint, json=payload)

    assert response.status_code == HTTPStatus.NOT_ACCEPTABLE


def test_create_profile_invalid_email(endpoint):
    """Create profile: 406 — Not Acceptable."""
    payload = dict(
        email='invalid_email',
        password='password',
    )

    response = requests.post(endpoint, json=payload)

    assert response.status_code == HTTPStatus.NOT_ACCEPTABLE
