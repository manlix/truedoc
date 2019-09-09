"""Аутентификация.
Ожидаемый возврат: 200 (OK).

Сценарий:
1) проходим положительную аутентификацию, указывая 'email' и 'password'."""
import requests

endpoint_profile = 'http://truedoc-app.localhost/auth/'
payload = dict(
    email='test@example.com',
    password='password',
)

r = requests.post(endpoint_profile, json=payload)

assert r.status_code == 200, f'Status code ({r.status_code}) is NOT 200. Reason: {r.text}'
assert 'access_token' in r.json()['result'], f'Cannot obtain access_token : {r.text}'
