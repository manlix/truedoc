"use strict";

$(document).ready(function () {

    function onError(msg) {

        $('#error').toggle(true);
        $('#error').html(msg);
    }

    function formSuccess(response) {

        let documents = "";

        for (let doc of response['result']) {
            documents += `<b>${doc['created_at']} (${doc['filename']}, ${doc['filesize']})</b><br>ID: ${doc['document_id']}<br><i>Digest: ${doc['digest']}</i><hr>`;
        }

        $('#ui')
            .empty()
            .html(documents);
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
                'width': '500px',
                'background-color': '#FCF4A3',
                'align': 'center',
                'text-align': 'center',
                'padding': '10px',
            });

    $('body').append(ui);

    $("#ui")
        .append(
            [
                '<h1>Список документов</h1>',
                '<div id="error"></div>',
                '<div id="success"></div>',
                '<div>Access TOKEN: <input id="token" autofocus required></div>',
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
        let token = $('#token')

        if (token.val().length == 0) {
            onError('Не указан Access Token.')
        } else {
            sendData();
        }
    }

    $('form').submit(function (event) {
        event.preventDefault();
        check_fields();
    });

    function sendData() {


        $.ajax({
            async: true,
            type: 'GET',
            url: 'http://truedoc-app.localhost/document/list',

            headers: {
                "Authorization": "Bearer " + $('#token').val(),
            },

            success: formSuccess,
            error: formFail,

            statusCode: {
                200: function () {
                }, // Документы получены.
                406: function () {
                }, // Какие-то поля заполнены неверно. Смотри: xhr.responseJSON.error_fields
                401: function () {
                }, // Аутентификация прошла неудачно
            }
        });
    }
});


