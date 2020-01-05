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
        value: $('#answer').val(),
        time_spent: (new Date().getTime() - startTime)/1000
    };
    console.log('zhopa', data.value)
//    if (isNaN(data.value)) {
//        alert('Некорректный ответ');
//        return;
//    }
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
                $('#answersHistory').html('');
                r.reverse().forEach(e=>{
                   const correctAnswer = e.correct_answer;
                   const exerciseRow = d.createElement('div');
                   exerciseRow.innerHTML = `
<div class="block__row ${e.is_correct ? 'primer-text--good':'primer-text--bad'}">
<span class="primer-text">${e.text} = </span>
                    <span class="primer-text">${e.given_answer}</span>${!e.is_correct ? `<span class="primer-text">${correctAnswer}</span>`:'' }
                    <span>Время решения: ${e.time_spent}</span>
</div>
                    `;
                   if (e.given_answer !== '') {
                       $('#answersHistory').append(exerciseRow);
                   }

                });
                $('#noHistoryMessage').hide();
                $('#answersHistory').show();
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
        $('#timerValue').text(Math.round(time));
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
