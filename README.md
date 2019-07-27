
# Правила проекта
* [Архитектура взаимодействия](#arch)
* [Действия](#actions)
* [Ответы] (#responses)

## Архитектура взаимодействия <a name="arch"></a>

* Используется [RESTful API](https://en.wikipedia.org/wiki/Representational_state_transfer#Applied_to_Web_services);
* **JSON** является основным форматом для входных и выходных данных (включая ошибки).

### Действия <a name="actions"></a>

Стандартные действия - [CRUD](https://en.wikipedia.org/wiki/Create,_read,_update_and_delete).

Действие | HTTP-метод | Контекст
-------- | ---------- | --------
Create   | POST       | Объект
Read     | GET        | Объект
Update   | PATCH      | Объект 
Delete   | DELETE     | Объект
  

#### Ответы <a name="responses"></a>

Каждый ответ содержит **status** со значением **success** (для успешных запросов) и **error** (для неудачных запросов) с уточняющей информацией в поле **description**.

* Простой положительный (HTTP-код: 200):
```json
{
  "status": "success"
}
```
         
* Простой отрицательный (HTTP-код: 400 и выше):
```json
{
  "status": "error",
  "description": "Краткое описание проблемы"
}
```


* Неудачный (HTTP-код: 400 и выше):

```json
{
  "status": "error",
  "description": "Bad request.",
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

> **status** _(str)_ = error - факт неудачного запроса ошибка;
>
> **description** _(str)_= краткое описание неудачного запроса;
>
> **errors_fields** _(dict)_ - факт на некорректные данные во входящем запросе, в полях;
>
> **errors_fields['входящее_поле']** _(list)_ - каждый элемент является описанием найденной ошибки в поле **входящее_поле**. Ошибок для каждого поля может быть несколько (зависит от кол-ва привязанных валидаторов);  

