'use strict';

const d = document;

function getPrimer() {
    $.ajax({
        method: 'GET',
        url: API_GET_PRIMER,
        contentType: 'application/json',
        crossDomain: true,
        beforeSend: function() {
        },
        complete: function() {
        },
        success: function (r) {
            console.log(r);
        }
    }).fail(function (err) {
        console.log('[AJAX] error ', err);
    });
}

function checkAnswer() {
    const data = {
        pk: parseInt($('#primer').data('pk')),
        value: parseFloat($('#primer').val())
    };
    if (isNaN(data.value)) {
        alert('Некорректный ответ');
        return;
    }
    $.ajax({
        method: 'POST',
        url: API_CHECK_ANSWER,
        contentType: 'application/json',
        crossDomain: true,
        data: JSON.stringify(data),
        beforeSend: function() {
        },
        complete: function() {
        },
        success: function (r) {
            console.log(r);
        }
    }).fail(function (err) {
        console.log([AJAX] error ``, err);
    });
}

function getAnswersHistory(){
    $.ajax({
        method: 'GET',
        url: API_GET_HISTORY,
        contentType: 'application/json',
        crossDomain: true,
        beforeSend: function() {
        },
        complete: function() {
        },
        success: function (r) {
            console.log(r);
        }
    }).fail(function (err) {
        console.log('[AJAX] error ', err);
    });
}

$(d).ready(function () {
    console.log('primer ready');

});
