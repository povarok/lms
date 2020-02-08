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
            if (r.url) {
                const { url, test_id } = r;
                window.location.href = `    ${url}${test_id}`;
            }
            console.log(r);
            window.test_id = r.test_id;
            window.exercise_index = r.exercise_index;
            $('#exerciseText').text(r.text);
            $('#answer').data('pk', r.pk);
            d.getElementById('answer').value = "";
            if (startTime === undefined) {
                startTime = new Date().getTime();
                timerLoop();
            } else {
                startTime = new Date().getTime();
                ClearСlock();
                timerLoop();
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
        exercise_index: window.exercise_index,
        time_spent: (new Date().getTime() - startTime)/1000
    };
    if (data.value == '') {
        alert('Введите ответ');
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
    var data = {
    test_id: window.test_id,
    exercise_index: window.exercise_index
    }
    $.ajax({
        method: 'POST',
        url: API_GET_HISTORY,
        headers: {
            "X-CSRFToken":CRSF_token
        },
        contentType: 'application/json',
        crossDomain: true,
        data: JSON.stringify(data),
        beforeSend: function() {
        },
        complete: function() {
        },
        success: function (r) {
            if (r.length === 0) {
                $('#noHistoryMessage').show();
                $('#answersHistory').hide();
            } else {
                $('#answersHistoryBody').html('');
                r.reverse().forEach(e=>{
                   const correctAnswer = e.correct_answer;
                   const exerciseRow = d.createElement('tr');
                   exerciseRow.innerHTML = `
                    <td>${e.text}</td>
                    <td>${e.given_answer}</td>
                    <td>${correctAnswer}</td>
                    <td>${e.time_spent}</td>
                    ${e.is_correct ? '<td><font color="#00cc00" size="5"><i class="icon-search glyphicon glyphicon-ok-circle"></i></font></td>':'<td><font color="#ff5050" size="5"><i class="icon-search glyphicon glyphicon-remove-circle"></i></font></td>'}
                    `;
                   if (e.given_answer !== '') {
                       $('#answersHistoryBody').append(exerciseRow);
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
//объявляем переменные
var base = 60;
var clocktimer, dateObj, dh, dm, ds, ms;
var readout = '';
var h = 1,
  m = 1,
  tm = 1,
  s = 0,
  ts = 0,
  ms = 0

//функция для очистки поля
function ClearСlock() {
  clearTimeout(clocktimer);
  h = 1;
  m = 1;
  tm = 1;
  s = 0;
  ts = 0;
  ms = 0;
  readout = '00:00:00';
  $('#timerValue').text(readout);
}

//функция для старта секундомера
function timerLoop() {
  var cdateObj = new Date();
  var t = (cdateObj.getTime() - startTime) - (s * 1000);
  if (t > 999) {
    s++;
  }
  if (s >= (m * base)) {
    ts = 0;
    m++;
  } else {
    ts = parseInt((ms / 100) + s);
    if (ts >= base) {
      ts = ts - ((m - 1) * base);
    }
  }
  if (m > (h * base)) {
    tm = 1;
    h++;
  } else {
    tm = parseInt((ms / 100) + m);
    if (tm >= base) {
      tm = tm - ((h - 1) * base);
    }
  }
  ms = Math.round(t / 10);
  if (ms > 99) {
    ms = 0;
  }
  if (ms == 0) {
    ms = '00';
  }
  if (ms > 0 && ms <= 9) {
    ms = '0' + ms;
  }
  if (ts > 0) {
    ds = ts;
    if (ts < 10) {
      ds = '0' + ts;
    }
  } else {
    ds = '00';
  }
  dm = tm - 1;
  if (dm > 0) {
    if (dm < 10) {
      dm = '0' + dm;
    }
  } else {
    dm = '00';
  }
  dh = h - 1;
  if (dh > 0) {
    if (dh < 10) {
      dh = '0' + dh;
    }
  } else {
    dh = '00';
  }
  readout = dh + ':' + dm + ':' + ds;
  $('#timerValue').text(readout);

  clocktimer = setTimeout(timerLoop, 1000);
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
