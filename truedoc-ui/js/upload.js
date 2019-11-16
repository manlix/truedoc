"use strict";

$(document).ready(function () {

    $('body').empty();

    var maxSize = 4 * 1024 * 1024; // 4MB

    function onError(msg) {

        $('#error').toggle(true);
        $('#error').html(msg);
    }

    function clearError() {

        $('#error').html("");

    }

    function formSuccess(response) {
        $('#ui')
            .empty()
            .html('Документ загружен!<br>document_id: ' + response['result'].document_id);
    }

    function formFail(xhr, ajaxOptions, thrownError) {
        console.log(xhr);
        console.log(ajaxOptions);
        console.log(thrownError);

        // TODO: read detailed errors from xhr.responseJSON.error_fields

        // 'About ''XMLHttpRequest': https://developer.mozilla.org/en-US/docs/Web/API/XMLHttpRequest

        if (xhr.readyState == 0) {
            onError('Сервис недоступен');
        } else if (xhr.status == 401) {
            onError('Ошибка авторизации');
        } else if (xhr.status == 406) {
            onError('Некоторые поля заполнены неверно');
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
                '<h1>Загрузка документа</h1>',
                '<div id="error"></div>',
                '<div id="success"></div>',
                '<div>Access TOKEN: <input id="token" autofocus required></div>',
                '<div>File: <input type="file" id="truedoc_document" autofocus required></div>',
                '<div>File description: <input id="truedoc_title" placeholder="optional field"></div>',
                '<div><br><input id="truedoc_submit" type="submit"></div>',
                '<progress value="0"></progress>',
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

    // See about 'selector': https://api.jquery.com/file-selector/
    $('#truedoc_document').on('change', function () {
        var selectedFile = this.files[0];

        if (selectedFile.size > maxSize) {

            $(this).val("");
            onError('Объём загружаемого документа превышает лимит в 4 МБ.');

        } else {

            clearError();
        }
    });


    $('form').submit(function (event) {
        event.preventDefault();
        sendData();
    });

    function sendData() {


        var data = new FormData();
        data.append("title", $('#truedoc_title').val());
        data.append("document", $('#truedoc_document')[0].files[0]);


        $.ajax({
            url: 'http://truedoc-app.localhost/document/',
            type: 'POST',

            data: data,

            cache: false,
            contentType: false,
            processData: false,

            headers: {
                "Authorization": "Bearer " + $('#token').val(),
            },

            success: formSuccess,
            error: formFail,

            statusCode: {
                202: function () {
                }, // Документ успешно загружен на обработку.
                406: function () {
                }, // Какие-то поля заполнены неверно. Смотри: xhr.responseJSON.error_fields
            },

            xhr: function () {
                var myXhr = $.ajaxSettings.xhr();
                if (myXhr.upload) {
                    // For handling the progress of the upload
                    myXhr.upload.addEventListener('progress', function (e) {
                        if (e.lengthComputable) {
                            $('progress').attr({
                                value: e.loaded,
                                max: e.total,
                            });
                        }
                    }, false);
                }
                return myXhr;
            }
        });
    }
});


