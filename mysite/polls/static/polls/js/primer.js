'use strict';

const d = document;

function getPrimer() {
    $.ajax({
        method: 'GET',
        url: API_GET_EXERCISE,
        contentType: 'application/json',
        crossDomain: true,
        beforeSend: function() {
        },
        complete: function() {
        },
        success: function (r) {
            console.log(r);
            $('#primer_text').text(r.text);
        }
    }).fail(function (err) {
        console.log(`[AJAX] error ${API_GET_EXERCISE}`, err);
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
        console.log(`[AJAX] error ${API_CHECK_ANSWER}`, err);
    });
}

function getAnswersHistory() {
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
        console.log(`[AJAX] error ${API_GET_HISTORY}`, err);
    });
}

function init() {
    getPrimer();
}

$(d).ready(function () {
    console.log('primer ready');
    init();

});
