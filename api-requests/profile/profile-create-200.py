"""Создание профиля (успех).
Должен возвращать: 200 (OK) или ошибку 409 (Conflict) в случае если профиль уже создан."""
import requests

endpoint = 'http://truedoc-app.localhost/profile/'
payload = dict(
    email='hello@example.com',
    password='password',
)

r = requests.post(endpoint, json=payload)

assert r.status_code in (
    200,  # 200 (OK)
    409,  # 409 (Conflict)
)
