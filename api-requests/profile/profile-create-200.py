"""Создание профиля (успех).
Ожидаемый возврат: 200 (OK).


Сценарий:
1) создаём профиль с email 'test@example.com' и паролем 'password';
2) удаляем созданный профиль.
"""
import requests

endpoint_profile = 'http://truedoc-app.localhost/profile/'
payload = dict(
    email='test@example.com',
    password='password',
)

r = requests.post(endpoint_profile, json=payload)

assert r.status_code == 200, f'Status code ({r.status_code}) is NOT 200. Cannot create profile: {r.text}'

profile_id = r.json()['result']['profile_id']

r = requests.delete(f'{endpoint_profile}{profile_id}')

assert r.status_code == 200, f'Status code ({r.status_code}) is NOT 200. Cannot delete profile ({profile_id}): {r.text}'
