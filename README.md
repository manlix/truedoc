
# Правила проекта
* [Системные требования](#system_requirements)
* [Разработческий стенд](#dev_mode)
    * [Работа с базой данных](#dev_mode.db)
    * [Работа с docker-compose](#dev_mode.docker_compose)
* [Архитектура взаимодействия](#arch)
* [Действия](#actions)
* [Ответы](#responses)
    * [Генераторы ответов](#responses.generators)
    * [Простой положительный](#responses.simple_positive)
    * [Простой отрицательный](#responses.simple_negative)
    * [Положительный](#responses.positive)
    * [Отрицательный](#responses.negative)
    * [HTTP коды ответов](#response_codes)
* [Инструменты](#tools)    
    * [Проверка кода на соответствие стандартам](#tools.code_standard)

## Системные требования <a name="system_requirements"></a>

* Python 3.7

## Разработческий стенд <a name="dev_mode"></a>

Необходимо создать **virtualenv** и установить пакеты из **requirements.txt**:
```sh
manlix@lab:~$ mkdir ~/venv && python3 -m venv ~/venv/truedoc
manlix@lab:~$ . ~/venv/truedoc
(truedoc) manlix@lab:~$ pip3 install -r ~/git/truedoc/requirements.txt
(truedoc) manlix@lab:~$ pushd ~/git/truedoc && python3 setup.py develop && popd

```

### Работа с базой данных <a name="dev_mode.db"></a>

Перед запуском **Truedoc** необходимо инициализировать базу данных:

```sh
# Upgrade to 'head' (latest revision)
manlix@lab:~/git/truedoc/truedoc$ alembic upgrade head
```

* Место хранения конфига: **truedoc/truedoc/alembic.ini**
* Место хранения ревизий: **truedoc/truedoc/alembic/versions/**
* Формат файла ревизии: **YYYYMMDDHHMMSS_revision_slug.py** _(список файлов ревизий всегда отсортирован)_

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

### Работа с docker-compose <a name="dev_mode.docker_compose"></a>

* Запустить Truedoc: 
```sh
manlix@lab:~/git/truedoc$ ./scripts/app.start.sh
```

* Стартовая: http://truedoc-app.localhost
* MySQL-сервер: truedoc-mysql.localhost:3306
* Веб-интерфейс к MySQL: http://truedoc-pma.localhost

Остановить контейнер с Truedoc:
```sh
manlix@lab:~/git/truedoc$ docker-compose -f docker-compose.dev.yml stop truedoc-app
```

Запустить контейнер с Truedoc:
```sh
manlix@lab:~/git/truedoc$ docker-compose -f docker-compose.dev.yml start truedoc-app
```

Посмотреть STDERR контейнера с Truedoc:
```sh
manlix@lab:~/git/truedoc$ docker-compose -f docker-compose.dev.yml logs truedoc-app
```

* Запустить bash-сессию внутри запущенного контейнера с MySQL: 
```sh
manlix@lab:~/git/truedoc$ docker-compose -f ./docker-compose.dev.yml exec truedoc-mysql bash
```

* Полностью остановить и зачистить (удалить контейнеры и образы) Truedoc: 
```sh
manlix@lab:~/git/truedoc$ ./scripts/docker.dropall.sh
```

## Архитектура взаимодействия <a name="arch"></a>

* Используется [RESTful API](https://en.wikipedia.org/wiki/Representational_state_transfer#Applied_to_Web_services);
* **JSON** является основным форматом для входных и выходных данных (включая ошибки);
* [Ответ](#responses) содержит специфичный HTTP-код.

## Действия <a name="actions"></a>

Используется подход [CRUD](https://en.wikipedia.org/wiki/Create,_read,_update_and_delete).

Действие | HTTP-метод | Контекст
-------- | ---------- | --------
Create   | POST       | Объект
Read     | GET        | Объект
Update   | PATCH      | Объект 
Delete   | DELETE     | Объект

## Ответы <a name="responses"></a>

Каждый ответ строится [генератором ответов](#responses.generators) и содержит специфичный [HTTP-код](#responses.http_codes) и **JSON** с обязательным полем **status** и значением **success** _(str)_ (для положительных) и **error** _(str)_ (для отрицательных) с уточняющей информацией в поле **description** _(str)_.

Типы ответов:
* [Простой положительный](#responses.simple_positive);
* [Простой отрицательный](#responses.simple_negative);
* [Положительный](#responses.positive);
* [Отрицательный](#responses.negative).

### Генераторы ответов <a name="responses.generators"></a>

Существует 2 функции для формирование ответов:

* **truedoc.response.success(http_code=200, description=None, \*\*kwargs)** - для положительных;
* **truedoc.response.failure(http_code=406, description=None, \*\*kwargs)** - для отрицательных.

### Простой положительный <a name="responses.simple_positive"></a>
* HTTP-код: **200** _(OK)_;
* Обязательные поля:
    * **status** _(str)_ = "success"

```json
{
  "status": "success"
}
```
         
### Простой отрицательный <a name="responses.simple_negative"></a>
* HTTP-код: **406** _(Not Acceptable)_ или **409** _(Conflict)_;
* Обязательные поля:
    * **status** _(str)_ = "error"
    * **description** _(str)_ = "краткое описание проблемы"

```json
{
  "status": "error",
  "description": "Краткое описание проблемы"
}
```

### Положительный <a name="responses.positive"></a>
* HTTP-код: **200** _(OK)_;
* Обязательные поля:
    * **status** _(str)_ = "success"
    * **result** _(dict)_ || _(list)_ || _(str)_ = result

```text
{
  "status": "success",
  "result": result
}
```

### Отрицательный <a name="responses.negative"></a> 
* HTTP-код: **406** _(Not Acceptable)_ и выше;
* Обязательные поля:
    * **status** _(str)_ = error - факт неудачного запроса ошибка
    * **description** _(str)_= краткое описание неудачного запроса
    * **errors_fields** _(dict)_ - факт на некорректные данные во входящем запросе, в полях
    * **errors_fields['входящее_поле']** _(list)_ - каждый элемент является описанием найденной ошибки в поле **входящее_поле**. Ошибок для каждого поля может быть несколько (зависит от кол-ва привязанных валидаторов) 

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

* **200** _(OK)_  - запрос принят и обработан (напр.: пользователь зарегистриррован);
* **400** _(Bad request)_ - некорректный запрос (напр.: невалидный JSON);
* **406** _(Not Acceptable)_ - запрос корректный, но есть ошибки в полях (напр.: при регистрации не указан пароль либо введён некорректный email);
* **409** _(Conflict)_ - конфликт при обработке запросе (напр.: профиль с таким email уже существует);
* **500** _(Internal Server Error)_ - проблема на стороне сервиса.

## Инструменты <a name="tools"></a>

### Проверка кода на соответствие стандартам <a name="tools.code_standard"></a>
Используется [Pylint](https://www.pylint.org/):

```shell
$ pylint code.py
```