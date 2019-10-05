import pytest
import requests


@pytest.fixture()
def endpoint():
    return 'http://truedoc-app.localhost/profile/'


def test_create_and_delete_profile(endpoint):
    payload = dict(
        email='test@example.com',
        password='password',
    )

    response = requests.post(endpoint, json=payload)

    assert response.status_code == 200  # Profile created

    profile_id = response.json()['result']['profile_id']

    response = requests.delete(f'{endpoint}{profile_id}')

    assert response.status_code == 200  # Profile deleted
