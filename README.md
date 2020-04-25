
* [Разработческий стенд](#dev_mode)
    * [Запуск Docker контейнеров](#dev_mode.docker_compose)
    * [Запуск в обычном режиме (docker-compose)](#dev_mode.simple_run)
    * [Запуск в режиме Debug (docker-compose)](#dev_mode.debug_run)
    * [Работа с базой данных](#dev_mode.db)
* [Архитектура взаимодействия](#arch)
* [Действия](#actions)
* [Использование очереди (Celery)](#queue)
* [Ответы](#responses)
    * [Генераторы ответов](#responses.generators)
    * [Простой положительный](#responses.simple_positive)
    * [Простой отрицательный](#responses.simple_negative)
    * [Простой отрицательный фатальный](#responses.simple_negative_fatal)
    * [Положительный синхронный](#responses.positive_synchronous)
    * [Положительный асинхронный](#responses.positive_asynchronous)
    * [Отрицательный](#responses.negative)
    * [HTTP коды ответов](#response_codes)
* [Обработка исключения](#handle_exceptions)
    * [Интеграция с Sentry](#handle_exceptions.sentry)
* [Тестирование](#tests)
* [Инструменты](#tools)    
    * [Проверка кода на соответствие стандартам](#tools.code_standard)
    * [Проверка кода на безопасность](#tools.code_safety)
    * [Обновление библиотек в requirements.txt до последних версий](#tools.update_requirements_txt)
* [Инструменты](#tools)
* [Известные проблемы](#issues)
    * [При доступе к БД: Unknown (generic) error from engine](#issues.populate_db)


## Разработческий стенд <a name="dev_mode"></a>

Единожды необходимо создать **virtualenv** и установить пакеты из **requirements.txt**:
```sh
manlix@lab:~$ mkdir ~/venv && python3 -m venv ~/venv/truedoc && . ~/venv/truedoc/bin/activate
(truedoc) manlix@lab:~$ python3 -m pip install -r ~/git/truedoc/requirements.txt

# В отличие от "install", для разработки используется "develop" - пакеты не устанавливаются, создаются ссылки.
(truedoc) manlix@lab:~$ pushd ~/git/truedoc && python3 setup.py develop && popd
```

### Запуск Docker контейнеров <a name="dev_mode.docker_compose"></a>

* Запустить Truedoc: 
```sh
manlix@lab:~/git/truedoc$ ./scripts/app.start.sh
```

* Стартовая: http://truedoc-app.localhost
* MySQL-сервер: truedoc-mysql.localhost:3306
* Веб-интерфейс к MySQL: http://truedoc-pma.localhost

Остановить контейнер с Truedoc:
```sh
manlix@lab:~/git/truedoc$ docker-compose stop truedoc-app
```

Запустить контейнер с Truedoc:
```sh
manlix@lab:~/git/truedoc$ docker-compose start truedoc-app
```

Посмотреть STDERR контейнера с Truedoc:
```sh
manlix@lab:~/git/truedoc$ docker-compose logs truedoc-app
```

* Запустить bash-сессию внутри запущенного контейнера с MySQL: 
```sh
manlix@lab:~/git/truedoc$ docker-compose exec truedoc-mysql bash
```

* Полностью остановить и зачистить (удалить контейнеры и образы) Truedoc: 
```sh
manlix@lab:~/git/truedoc$ ./scripts/docker.dropall.sh
```

### Запуск в обычном режиме (docker-compose) <a name="dev_mode.simple_run"></a>

Создание конфигурации:
* `Run` -> `Edit Configurations...` -> `+` -> `Docker` -> `Docker Compose`

Параметры для заполнения:
* *Server*: `Docker`
* *Compose file(s)*: `./docker-compose.yml`
* *Service(s):*: `truedoc-app`
* *Environment variables*: `(empty)`

**Options**

* `[ ]` *--build, force build images*

Запуск:
* `Run` -> `Run...` -> `(выбрать только что созданную конфигураци)`

### Запуск в режиме Debug (docker-compose) <a name="dev_mode.debug_run"></a>

Создание конфигурации:
* `Run` -> `Edit Configurations...` -> `+` -> `Flask Server`

Параметры для заполнения:
* *Target type*: `[V] Module name`
* *Target*: `truedoc.website`
* *Application*: `app`
* *Additional options*: `--host=0.0.0.0`
* *FLASK_ENV*: `development`
* *FLASK_DEBUG*: `[V]`

**Environment**
* *Environment variables*: `(empty)`
* *Python Interpretator*: `Remove Python 3.8.0 Docker Compose (truedoc-app at [/home/manlix/git/truedoc/docker-compose.yml])`
* *Interpretator options*: `(empty)`
* *Working directory*: `(empty)`
* *Path mappings*: `(empty)`
* `[V]` *Add content roots to PYTHONPATH*
* `[V]` *Add source roots to PYTHONPATH*

Запуск:
* `Run` -> `Run...` -> `(выбрать только что созданную конфигураци)`

**Docker Compose**
* *Command and options*: `(default)`
* *Command preview: `(default)`

### Работа с базой данных <a name="dev_mode.db"></a>

Перед запуском **Truedoc** необходимо инициализировать базу данных:

```sh
# Upgrade to 'head' (latest revision)

manlix@lab:~/git/truedoc$ docker-compose exec truedoc-app sh
/var/lib/truedoc # cd truedoc/ && PYTHONPATH=.. alembic upgrade head && exit
manlix@lab:~/git/truedoc$
```

* Место хранения конфига: `truedoc/truedoc/alembic.ini`
* Место хранения ревизий: `truedoc/truedoc/alembic/versions/`
* Формат файла ревизии: `YYYYMMDDHHMMSS_revision_slug.py` _(список файлов ревизий всегда отсортирован)_

Создание новой ревизии:

**ВАЖНО:** после создания необходимо проверить сгенерированный код _(**alembic** может не распознавать некоторые изменения в моделях и базе данных)_.
```sh
manlix@lab:~/git/truedoc/truedoc$ alembic revision -m 'Init DB' --autogenerate
```

Текущая ревизия в базе данных:
```sh
# Show 'current revision' in database
manlix@lab:~/git/truedoc/truedoc$ alembic current
```

Даунгрейд на 1 ревизию:
```sh
# Downgrade to '-1 revision'
manlix@lab:~/git/truedoc/truedoc$ alembic downgrade -1
```

Апгрейд на 1 ревизию:
```sh
# Upgrade to '+1 revision'
manlix@lab:~/git/truedoc/truedoc$ alembic upgrade +1
```

## Архитектура взаимодействия <a name="arch"></a>

* Используется [RESTful API](https://en.wikipedia.org/wiki/Representational_state_transfer#Applied_to_Web_services);
* `JSON` является основным форматом для входных и выходных данных (включая ошибки);
* [Ответ](#responses) содержит специфичный HTTP-код.

## Действия <a name="actions"></a>

Используется подход [CRUD](https://en.wikipedia.org/wiki/Create,_read,_update_and_delete).

Действие | HTTP-метод | Контекст
-------- | ---------- | --------
Create   | POST       | Объект
Read     | GET        | Объект
Update   | PATCH      | Объект 
Delete   | DELETE     | Объект

## Использование очереди <a name="queue"></a>

[Celery](https://docs.celeryproject.org) — распределённая очередь задач, используется для обработки загруженных файлов. Задачи сформированы в модуле `truedoc.tasks`.

Запуск `worker'а` происходит при запуске контейнера [truedoc-celery-worker](https://github.com/manlix/truedoc/blob/c63756f4db25b1959386aefcd162b0aab8e84ff9/docker-compose.yml#L42).

Запуск на локальном компьютере, при поднятом RabbitMQ:
```bash
(truedoc) manlix@lab:~/git/truedoc$ celery -A truedoc.tasks worker -l info --broker="amqp://guest:guest@localhost"
```


## Ответы <a name="responses"></a>

Каждый ответ строится [генератором ответов](#responses.generators) и содержит специфичный [HTTP-код](#responses.http_codes) и **JSON** с обязательным полем **status** и значением **success** _(str)_ (для положительных) и **error** _(str)_ (для отрицательных) с уточняющей информацией в поле **description** _(str)_.

Типы ответов:
* [Простой положительный](#responses.simple_positive);
* [Простой отрицательный](#responses.simple_negative);
* [Простой отрицательный фатальный](#responses.simple_negative_fatal);
* [Положительный](#responses.positive);
* [Отрицательный](#responses.negative).

### Генераторы ответов <a name="responses.generators"></a>

Существует 2 функции для формирование ответов:

* `truedoc.response.success(http_code=200, description=None, **kwargs)` - для положительных;
* `truedoc.response.failure(http_code=406, description=None, **kwargs)` - для отрицательных.

### Простой положительный <a name="responses.simple_positive"></a>
* HTTP-код: `200 (OK)`;
* Обязательные поля:
    * `status` _(str)_ = `success`

```json
{
  "status": "success"
}
```
         
### Простой отрицательный <a name="responses.simple_negative"></a>
* HTTP-код: `406 (Not Acceptable)` или `409 (Conflict)`;
* Обязательные поля:
    * `status` _(str)_ = `error`
    * `description` _(str)_ = `краткое описание проблемы`

```json
{
  "status": "error",
  "description": "Краткое описание проблемы"
}
```

### Простой отрицательный фатальный <a name="responses.simple_negative_fatal"></a>

Отличается от `простого отрицательного` наличием поля `internal_error`, свидетельствующим, что проблема произошла на стороне сервера (напр.: недоступна БД).

* HTTP-код: `500 (Internal Server Error)`;
* Обязательные поля:
    * `status` _(str)_ = `error`
    * `internal_error` (bool) = `True`
    * `description` _(str)_ = `краткое описание проблемы`

```json
{
  "status": "error",
  "internal_error": true,        
  "description": "Краткое описание проблемы"
}
```

### Положительный <a name="responses.positive"></a>

#### Положительны синхронный <a name="responses.positive_synchronous"></a>

* HTTP-код: `200` _(OK)_;
* Обязательные поля:
    * `status` _(str)_ = `success`
    * `result` _(dict)_ || _(list)_ || _(str)_ = `result`

```text
{
  "status": "success",
  "result": result
}
```

#### Положительны асинхронный <a name="responses.positive_asynchronous"></a>

**Используется только при загрузке документа.**

* HTTP-код: `202` _(Accepted)_;
* Обязательные поля ответа:
    * `status` _(str)_ = `success`
    * `result` _(dict)_ = `result`
    * `result['state']` _(str)_ = `PENDING`   <--- запрос принят и будет обработан асинхронно

Пример ответа:
```json
{
  "result": {
    "document_id": "82d23088-e3d5-4c1b-8949-a5edafb2955d",
    "filename": "test.txt",
    "profile_id": "0cfbd0a0-c46f-4ddb-8f01-f07622765969",
    "state": "PENDING",
    "title": "my test file"
  },
  "status": "success"
}
```

### Отрицательный <a name="responses.negative"></a> 
* HTTP-код: `406 (Not Acceptable)` и выше, но не больше `499`;
* Обязательные поля:
    * `status` _(str)_ = `error` — факт неудачного запроса ошибка
    * `description` _(str)_= `краткое описание неудачного запроса`
    * `errors_fields` _(dict)_ — факт на некорректные данные во входящем запросе, в полях
    * `errors_fields['входящее_поле']` _(list)_ — каждый элемент является описанием найденной ошибки в поле **входящее_поле**. Ошибок для каждого поля может быть несколько (зависит от кол-ва привязанных валидаторов) 

```json
{
  "status": "error",
  "description": "Bad request",
  "error_fields": {
    "email": [
      "Incorrect email."    
    ],
    "password": [
      "Missing data for required field."
    ]  
  } 
}
``` 

### HTTP коды ответов <a name="responses.http_codes"></a>

* `200 (OK)`  - запрос принят и обработан (напр.: пользователь зарегистриррован);
* `202` (Accepted) — запрос принят, но будет дополнительно (асинхронно) обработан (`worker'ом`);
* `400 (Bad request)` - некорректный запрос (напр.: невалидный JSON);
* `406 (Not Acceptable)` - запрос корректный, но есть ошибки в полях (напр.: при регистрации не указан пароль либо введён некорректный email);
* `409 (Conflict)` - конфликт при обработке запросе (напр.: профиль с таким email уже существует);
* `500 (Internal Server Error)` - проблема на стороне сервиса.

## Обработка исключений <a name="handle_exceptions"></a>

Чтобы при ∀ проблемах на стороне сервера отдавать клиенту `JSON`, вместо обычного текста (например: `500 (Internal Server Error)` необходимо градировать типы исключений и отдавать соответствующий ответ:

* `TruedocError` — проблемы уровня проекта (указанный пользователь не ∃, не введены обязательные поля, ...); 
* `SQLAlchemyError` — проблемы при работе с БД (ошибки при доступе к БД);
* `MarshmallowError` — проблемы валидации данных;
* `Exception` — ∀ другие проблемы.

Обработчики зарегистрированы в `truedoc.app`:

```python
@app.errorhandler(TruedocError)
def handle_exception_truedocerror(exc):
    ...

@app.errorhandler(SQLAlchemyError)
def handle_exception_sqlalchemyerror(exc):
    ...

@app.errorhandler(MarshmallowError)
def handle_exception_validationerror(exc):
    ...

@app.errorhandler(Exception)
def handle_exception_unknown(exc):
    ...
```

### Интеграция с Sentry <a name="handle_exceptions.sentry"></a>

В качестве инструмента выявления проблем (исключений) в реал-тайме используется (Sentry)[https://sentry.io].

Используемые интеграции:
* [Flask](https://docs.sentry.io/platforms/python/flask/)
* [SQLAlchemy](https://docs.sentry.io/platforms/python/sqlalchemy/)
* [Celery — на стороне `worker'а`](https://docs.sentry.io/platforms/python/celery/)

## Тестирование <a name="tests"></a>

Для тестирование используется [pytest](https://docs.pytest.org):

```shell
(truedoc) manlix@lab:~/git/truedoc$ ./scripts/tests.run.sh
```

Для генерации HTML-отчёта по покрытию кода тестами:

```shell
(truedoc) manlix@lab:~/git/truedoc$ ./scripts/tests.coverage-save.sh
```

Отчёт сохраняется в `htmlcov`, для просмотра открыть `htmlcov/index.html`.

## Инструменты <a name="tools"></a>

### Проверка кода на соответствие стандартам <a name="tools.code_standard"></a>
Используется [Pylint](https://www.pylint.org):

```shell
$ pylint code.py
```

### Проверка кода на безопасность <a name="tools.code_safety"></a>
Используется [Bandit](https://github.com/PyCQA/bandit):

```shell
$ bandit code.py
```

### Обновление библиотек в requirements.txt до последних версий <a name="tools.update_requirements_txt"></a>

```shell
(truedoc) manlix@lab:~/git/truedoc$ pur 
Updated alembic: 1.1.0 -> 1.2.0
Updated marshmallow: 3.0.5 -> 3.2.0
Updated sentry-sdk: 0.11.2 -> 0.12.2
All requirements up-to-date.
```

## Инструменты <a name="tools"></a>

* Языки: 
    * [Python](https://www.python.org)
    * [Bash](https://www.gnu.org/software/bash/)
 
* Библиотеки для Python:
    * [Alembic](https://alembic.sqlalchemy.org) — миграция базы данных
    * [Celery](https://docs.celeryproject.org) — распределённая очередь задач
    * [Flask](https://palletsprojects.com/p/flask/) — основной framework
    * [Marshmallow](https://marshmallow.readthedocs.io) — валидация моделей
    * [PyJWT](https://github.com/jpadilla/pyjwt) — работа с токенами JWT (JSON Web Token)
    * [PyMySQL](https://github.com/PyMySQL/PyMySQL) — работа с MySQL
    * [Requests](http://python—requests.org) — тестовые запросы к API
    * [Sentry](https://github.com/getsentry/sentry-python) — платформа мониторинга проблем в коде (исключения) в реал-тайме
    * [SQLAlchemy](https://www.sqlalchemy.org) — ORM для работы с базой данных

* Plugins для PyCharm:
    * [shellcheck](https://plugins.jetbrains.com/plugin/10195-shellcheck/) — анализ shell скриптов утилитой `shellcheck`
    * [String Manipulation](https://plugins.jetbrains.com/plugin/2162-string-manipulation/) — сортировка строк и прочии манипуляции с текстом

* Утилиты:
    * [Bandit](https://github.com/PyCQA/bandit) — проверка безопасности Python кода
    * [Pylint](https://www.pylint.org) — проверка Python кода на соответствие стандартам
    * [pytest](https://docs.pytest.org) — тестирование Python кода
    * [pytest-cov](https://pytest-cov.readthedocs.io) — проверка проекта на покрытие кода тестами

* Другое:

    * [CORS](https://learn.javascript.ru/fetch-crossorigin) — политика CORS
    * [Docker](https://www.docker.com) — контейнеры
    * [docker-compose](https://docs.docker.com/compose/) — декларативная организация контейнеров
    * [Git](https://git—scm.com) — управление исходным кодом
    * [HTTP](https://en.wikipedia.org/wiki/Hypertext_Transfer_Protocol) — канал связи для API
    * [Jenkins](https://jenkins.io) — CI/CD
    * [jQuery](https://jquery.com) — Javascript-библиотека, для использования AJAX
    * [JSON](https://en.wikipedia.org/wiki/JSON) — для передачи структур в видел JSON
    * [nginx](https://nginx.org) — обратный прокси—сервер поверх контейнеров
    * [pur](https://github.com/alanhamlett/pip-update-requirements) — обновление requirements.txt до последних версий

## Известные проблемы <a name="issues"></a>

### При доступе к БД: Unknown (generic) error from engine <a name="issues.populate_db"></a>

Проблема возникает из-за проблем с правами доступа на `mysql-data` при запуске Docker-контейнера `truedoc-mysql`:
```
pymysql.err.InternalError: (1030, "Got error 168 - 'Unknown (generic) error from engine' from storage engine")

```

*Решение:*

```
(truedoc) manlix@lab:~/git/truedoc$ sudo chown -R manlix:manlix ./mysql-data
```
