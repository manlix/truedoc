$(document).ready(function(){

    function onError(msg) {

        $('#error').toggle(true);
        $('#error').html(msg);
    }

    function formSuccess(response) {

        $('#ui')
            .empty()
            .html('Аутентификация прошла успешно!<br>Access TOKEN: ' + response['result'].access_token + '<br>Refresh TOKEN: ' + response['result'].refresh_token);
    }

    function formFail(xhr, ajaxOptions, thrownError) {
        console.log(xhr);
        console.log(ajaxOptions);
        console.log(thrownError);

        // TODO: read detailed errors from xhr.responseJSON.error_fields

        // 'About ''XMLHttpRequest': https://developer.mozilla.org/en-US/docs/Web/API/XMLHttpRequest

        if (xhr.readyState == 0) {
            onError('Сервис недоступен');
        } else if (xhr.status == 406) {
            onError('Некоторые поля заполнены неверно');
        } else if (xhr.status == 401) {
            onError('Аутентификация прошла неудачно');
        }
    }

    var ui = $('<div></div>')
            .attr('id', 'ui')
            .css(
                {
                    'border': '10px green solid',
                    'width':'500px',
                    'background-color': '#FCF4A3',
                    'align': 'center',
                    'text-align': 'center',
                    'padding': '10px',
            });

    $('body').append(ui);

    $("#ui")
        .append(
            [
                '<h1>Аутентификация</h1>',
                '<div id="error"></div>',
                '<div id="success"></div>',
                '<div>Email:</div>',
                '<input id="email" name="email" placeholder="email@example.com" autofocus>',
                '<div>Пароль:</div>',
                '<div><input id="password" name="password" type="password"></div>',
                '<div><br><input type="submit"></div>',
            ]
        )
        .wrap('<form></form>');

    $('#error').css(
    {
        'color': '#ffffff',
        'background-color': '#ff0000',
        'display': 'none',

    });

    $('#success').css(
    {
        'color': '#ffffff',
        'background-color': 'green',
        'display': 'none',

    });


    function check_fields() {
        email = $('#email')
        password = $('#password')

        if (email.val().length == 0) {
            onError('Не введён email.')
        }

        else if (password.val().length == 0) {
            onError('Не введён пароль.');
        } else {
            sendData();
        }
    }

    $('form').submit(function(event) {
        event.preventDefault();
        check_fields();
    });

    function sendData() {

        var arr = {
            email: $('form input[name=email]').val(),
            password: $('form input[name=password]').val(),
        }

        $.ajax({
            async: true,
            contentType: 'application/json; charset=utf-8',
            data: JSON.stringify(arr),
            dataType: 'json',
            type: 'POST',
            url: 'http://truedoc-app.localhost/auth/',

            success: formSuccess,
            error: formFail,

            statusCode: {
                200: function() { }, // Регистрация прошла успешно.
                406: function() { }, // Какие-то поля заполнены неверно. Смотри: xhr.responseJSON.error_fields
                401: function() { }, // Аутентификация прошла неудачно
            }
        });
    }
});


