import time

from http import HTTPStatus

import pytest
import requests

import truedoc.constants

res = {}


@pytest.fixture(autouse=True)
def profile_lifecycle():
    """Create and delete profile during session."""

    payload = dict(
        email='test@example.com',
        password='password',
    )

    # Create profile
    r = requests.post('http://truedoc-app.localhost/profile/', json=payload)
    assert 200 == r.status_code, f'Status code ({r.status_code}) is NOT 200. Cannot create profile: {r.text}'

    profile_id = r.json()['result']['profile_id']

    res.update({
        'profile_id': profile_id,
    })

    yield

    # Delete profile
    r = requests.delete(f'http://truedoc-app.localhost/profile/{profile_id}')
    assert r.status_code == HTTPStatus.OK  # Profile deleted (200)


@pytest.fixture()
def endpoints():
    """Endpoints."""
    return {
        'document': 'http://truedoc-app.localhost/document/',
        'profile': 'http://truedoc-app.localhost/profile/',
    }


def test_document_lifecycle(endpoints):
    """Document lifecycle."""
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

    # Upload document
    r = requests.post(endpoints['document'], **payload)

    assert 202 == r.status_code, f'Status code ({r.status_code}) is NOT 202. Cannot create document: {r.text}'

    document_id = r.json()['result']['document_id']

    res.update({
        'document_id': document_id,
    })

    # Waiting that document task state == 'SUCCESS'
    for _ in range(5):
        r = requests.get(f'http://truedoc-app.localhost/document/{document_id}/state')
        assert 200 == r.status_code, f'Status code ({r.status_code}) is NOT 200. Cannot get task ({document_id}) state: {r.text}'

        assert 'result' in r.json(), f'Not found "result" in response: {r.text}'
        assert 'state' in r.json()['result'], f'Not found "state" in response["result"]: {r.text}'

        assert r.json()['result']['state'] in truedoc.constants.JOB_STATE.ALL_STATES, f'Unknown task state: {r.text}'

        if r.json()['result']['state'] == truedoc.constants.JOB_STATE.SUCCESS:
            break

        time.sleep(1)
    else:
        raise Exception('5 attempts to get task state exceeded')

    # Get document
    r = requests.get(f'{endpoints["document"]}')

    assert 200 == r.status_code, f'Status code ({r.status_code}) is NOT 200. Cannot load document ({res["document_id"]}): {r.text}'

    # Delete document
    r = requests.delete(f'{endpoints["document"]}{res["document_id"]}')

    assert r.status_code == 200, f'Status code ({r.status_code}) is NOT 200. Cannot delete document ({res["document_id"]}): {r.text}'
