from http import HTTPStatus

import pytest
import requests


@pytest.fixture(autouse=True)
def profile_lifecycle():
    """Create and delete profile during session."""

    payload = dict(
        email='test@example.com',
        password='password',
    )

    # Create profile
    response = requests.post('http://truedoc-app.localhost/profile/', json=payload)
    assert response.status_code == HTTPStatus.OK  # Profile created (200)
    profile_id = response.json()['result']['profile_id']

    yield

    # Delete profile
    response = requests.delete(f'http://truedoc-app.localhost/profile/{profile_id}')
    assert response.status_code == HTTPStatus.OK  # Profile deleted (200)


@pytest.fixture()
def endpoint():
    """Endpoint for 'auth'."""
    return 'http://truedoc-app.localhost/auth/'


def test_auth_success(endpoint):
    """Test success auth."""

    payload = dict(
        email='test@example.com',
        password='password',
    )

    response = requests.post(endpoint, json=payload)

    assert response.status_code == HTTPStatus.OK, f'Status code ({response.status_code}) is NOT 200. Cannot make auth by login/password: {response.text}'


def test_auth_invalid_password(endpoint):
    """Test failure auth."""

    payload = dict(
        email='test@example.com',
        password='INVALID_PASSWORD',
    )

    response = requests.post(endpoint, json=payload)

    assert response.status_code == HTTPStatus.UNAUTHORIZED, f'Status code ({response.status_code}) is NOT 401. Should get failure instead successful response: {response.text}'
