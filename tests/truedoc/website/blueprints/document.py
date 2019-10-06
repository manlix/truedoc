from http import HTTPStatus

import pytest
import requests

res = {}


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
    res.update({
        'profile_id': profile_id,
    })

    yield

    # Delete profile
    response = requests.delete(f'http://truedoc-app.localhost/profile/{profile_id}')
    assert response.status_code == HTTPStatus.OK  # Profile deleted (200)


@pytest.fixture()
def endpoint_document():
    """Endpoint for 'document'."""
    return 'http://truedoc-app.localhost/document/'


@pytest.fixture()
def endpoint_profile():
    """Endpoint for 'auth'."""
    return 'http://truedoc-app.localhost/profile/'


def test_upload_1kb_document(endpoint_document):
    """Upload 1KB document."""
    payload = {
        'data': {
            'profile_id': res['profile_id'],
            'title': 'Document Simple Title: 1KB',
        },
        'files': [
            (
                'document',
                (
                    'file_1KB.txt',
                    1024 * 'x',
                )
            ),
        ]
    }

    response = requests.post(endpoint_document, **payload)

    assert response.status_code == HTTPStatus.ACCEPTED, f'Status code ({response.status_code}) is NOT 202. Cannot create document: {response.text}'

    res.update({
        'document_id': response.json()['result']['document_id'],
    })


def test_get_uploaded_document(endpoint_document):
    """Get uploaded document."""
    response = requests.get(f'{endpoint_document}{res["document_id"]}')

    assert response.status_code == 200, f'Status code ({response.status_code}) is NOT 200. Cannot load document ({res["document_id"]}): {response.text}'


def test_delete_uploaded_document(endpoint_document):
    """Delete uploaded document."""
    response = requests.delete(f'{endpoint_document}{res["document_id"]}')

    assert response.status_code == 200, f'Status code ({response.status_code}) is NOT 200. Cannot delete document ({res["document_id"]}): {response.text}'
