"""Аутентификация.
Ожидаемый возврат: 401 (Unauthorized).

Сценарий:
1) проходим отрицательную аутентификацию, указывая 'email' и 'password'."""
import requests

endpoint_profile = 'http://truedoc-app.localhost/auth/'
payload = dict(
    email='test@example.com',
    password='INVALID_PASSWORD',
)

r = requests.post(endpoint_profile, json=payload)

assert r.status_code == 401, f'Status code ({r.status_code}) is NOT 401. Reason: {r.text}'
