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
            $('#exerciseText').text(r.text);
            $('#answer').data('pk', r.pk);
            if (startTime === undefined) {
                startTime = new Date().getTime();
                timerLoop();
            } else {
                startTime = new Date().getTime();
            }
        }
    }).fail(function (err) {
        console.log(`[AJAX] error ${API_GET_EXERCISE}`, err);
    });
}

function checkAnswer() {
    const data = {
        pk: parseInt($('#answer').data('pk')),
        value: parseFloat($('#answer').val()),
        time_spent: new Date().getTime() - startTime
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
        headers: {
            "X-CSRFToken":CRSF_token
        },
        data: JSON.stringify(data),
        beforeSend: function() {
        },
        complete: function() {
        },
        success: function (r) {
            console.log(r);
            getPrimer();
            getAnswersHistory();
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
            if (r.length === 0) {
                $('#noHistoryMessage').show();
                $('#answersHistory').hide();
            } else {
                r.forEach(e=>{
                    const correctAnswer = e.correct_answer;
                   const exerciseRow = d.createElement('div');
                   exerciseRow.innerHTML = `
                    <span class="primer-text ${e.is_correct ? 'primer-text--good':'primer-text--bad'}">${e.text}</span>
                    <span class="answer">${e.user_answer}</span>${!e.is_correct ? `<span class="answer">${correctAnswer}</span>`:'' }`;
                   $('#answersHistory').append(exerciseRow);
                });
                $('#noHistoryMessage').show();
                $('#answersHistory').hide();
            }
        }
    }).fail(function (err) {
        console.log(`[AJAX] error ${API_GET_HISTORY}`, err);
    });
}

let time = 0;
let startTime;
function timerLoop() {
    time = Math.round((new Date().getTime() - startTime)/1000 * 100) / 100;
    if (time/60 > 1) {
        $('#timerValue').text(Math.round(time/60 * 10)/10);
        $('#timerUnit').text('м.');
    } else {
        $('#timerValue').text(time);
        $('#timerUnit').text('c.');
    }
    setTimeout(timerLoop,1000);
}

function attachListeners() {
    $('#checkAnswer').click(function () {
        checkAnswer();
    });
}

function init() {
    attachListeners();
    getPrimer();
    getAnswersHistory();
}

$(d).ready(function () {
    console.log('primer ready');
    init();

});
