
# Правила проекта
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
  "result": "result"
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