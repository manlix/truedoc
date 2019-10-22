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

    assert response.status_code == HTTPStatus.OK, f'Status code ({response.status_code}) is NOT 200. Cannot create new profile: {response.text}'

    profile_id = response.json()['result']['profile_id']

    response = requests.delete(f'{endpoint}{profile_id}')

    assert response.status_code == HTTPStatus.OK, f'Status code ({response.status_code}) is NOT 200. Cannot delete profile ({profile_id}): {response.text}'


def test_create_profile_bad_request(endpoint):
    """Create profile: 400 — Bad request."""
    headers = {
        'Content-type': 'application/json'
    }

    response = requests.post(endpoint, headers=headers)

    assert response.status_code == HTTPStatus.BAD_REQUEST, f'Status code ({response.status_code}) is NOT 400. Should get failure (Bad request) instead: {response.text}'


def test_create_profile_not_acceptable(endpoint):
    """Create profile: 406 — Not Acceptable."""
    payload = dict(
        email='test@example.com',
    )

    response = requests.post(endpoint, json=payload)

    assert response.status_code == HTTPStatus.NOT_ACCEPTABLE, f'Status code ({response.status_code}) is NOT 406. Should get failure (Not acceptable) instead: {response.text}'


def test_create_profile_invalid_email(endpoint):
    """Create profile: 406 — Not Acceptable."""
    payload = dict(
        email='invalid_email',
        password='password',
    )

    response = requests.post(endpoint, json=payload)

    assert response.status_code == HTTPStatus.NOT_ACCEPTABLE, f'Status code ({response.status_code}) is NOT 406. Should get failure (Not acceptable) instead: {response.text}'