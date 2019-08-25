"""Создание документа (успех).
Должен возвращать: 200 (OK)."""
import requests

from truedoc import constants

endpoint_document = 'http://truedoc-app.localhost/document/'
endpoint_profile = 'http://truedoc-app.localhost/profile/'

payload = dict(
    email='test@example.com',
    password='password',
)

r = requests.post(endpoint_profile, json=payload)

assert r.status_code == 200, f'Status code ({r.status_code}) is NOT 200. Cannot create profile: {r.text}'

profile_id = r.json()['result']['profile_id']

# Upload file with size=1KB
payload = {
    'data': {
        'profile_id': profile_id,
        'title': 'Document Simple Title: 1KB',
    },
    'files': [
        (
            'document',
            (
                'file_1KB.txt',
                1 * constants.SIZE.KILOBYTE * 'x',
            )
        ),
    ]
}

r = requests.post(endpoint_document, **payload)

assert r.status_code == 200, f'Status code ({r.status_code}) is NOT 200. Cannot create document: {r.text}'

document_id = r.json()['result']['document_id']

r = requests.get(f'{endpoint_document}{document_id}')

assert r.status_code == 200, f'Status code ({r.status_code}) is NOT 200. Cannot load document ({document_id}): {r.text}'

r = requests.delete(f'{endpoint_document}{document_id}')

assert r.status_code == 200, f'Status code ({r.status_code}) is NOT 200. Cannot delete document ({document_id}): {r.text}'

r = requests.delete(f'{endpoint_profile}{profile_id}')

assert r.status_code == 200, f'Status code ({r.status_code}) is NOT 200. Cannot delete profile ({profile_id}): {r.text}'
