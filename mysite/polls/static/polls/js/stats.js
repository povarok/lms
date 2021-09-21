
function getDataset() {
    var selector = document.getElementById("apparatus-selector");
    var selectedApparatus = selector.options[selector.selectedIndex].text;
    var data = {
    trainingApparatus: selectedApparatus,
    }
    $.ajax({
        method: 'POST',
        url: '/api_get_stats/',
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
            correctPercentageChart(r)
            exerciseChart(r)
            learningCurve(r)
            learningCurveTests(r)
        }
    }).fail(function (err) {
        console.log(`[AJAX] error `, err);
    });
}

function correctPercentageChart(dataset) {
    var data = $.map(dataset.tests, function(item, index) {
        return [[index +1 , (item.correct_answers / item.apparatus.exercises_amount) * 100]]
    });
    Highcharts.chart('myChart', {

        chart: {
            zoomType: 'x'
        },
        rangeSelector: {
            selected: 1
        },
        legend: {
            enabled: false
        },
        exporting: { enabled: false },
        title: {
            text: "Процент верных ответов",
        },

        series: [{
            type: 'column',
            name: 'Процент верных ответов',
            data: data,
            tooltip: {
                valueDecimals: 2
            }
        }],
        yAxis: [{
            title: {
                text: 'Процент верных ответов',
                style: {
                    fontSize: '16px',
                }
            },
            max: 100,
        }],
        xAxis: [{
            allowDecimals: false,
            title: {
                text: 'Пройденные тесты, номер попытки',
                style: {
                    fontSize: '16px',
                }
            }
        }],
        plotOptions: {
            column: {
                minPointLength: 3
            }
        }
    });
}

function getSeconds(string) {
    var a = string.split(':');
    var seconds = (+a[0]) * 60 * 60 + (+a[1]) * 60 + (+a[2]);
    return seconds
}

String.prototype.toHHMMSS = function () {
    var sec_num = parseFloat(this); // don't forget the second param
    var hours   = Math.floor(sec_num / 3600);
    var minutes = Math.floor((sec_num - (hours * 3600)) / 60);
    var seconds = sec_num - (hours * 3600) - (minutes * 60);

    if (hours   < 10) {hours   = "0"+hours;}
    if (minutes < 10) {minutes = "0"+minutes;}
    if (seconds < 10) {seconds = "0"+seconds;}
    return hours+':'+minutes+':'+seconds;
}

function exerciseChart(dataset) {
    var data = $.map(dataset.tests, function(item, index) {
        var exercises = $.map(item.exercises, function(exercise) {
            return [exercise]
        })
        var result = exercises.filter(exercise => {
            return exercise.answer_is_correct === true
        })
        return result;
    });
    var newData = data.map(function(item, index) {
        return [index+1, item.time_spent]
    })
    Highcharts.chart('myChart2', {

        chart: {
            zoomType: 'x'
        },
        rangeSelector: {
            selected: 1
        },
        legend: {
            enabled: false
        },
        exporting: { enabled: false },
        title: {
            text: "Время верного решения примера",
        },
        colors: [
            'rgba(35, 199, 35, 0.6)',
        ],

        series: [{
            type: 'areaspline',
            fillOpacity: 0.4,
            name: 'Время верного решение примера',
            data: newData.map(function(item) {
                return item[1] = getSeconds(item[1])
            }),
            tooltip: {
                valueDecimals: 2
            }
        }],
        yAxis: [{
            labels: {
                formatter: function() {
                    return (this.value+'').toHHMMSS()
                }
            },
            title: {
                text: 'Время, потраченное на поиск верного решения, сек',
                style: {
                    fontSize: '16px',
                }
            },
        }],
        xAxis: [{
            allowDecimals: false,
            title: {
                text: 'Успешно решенные примеры',
                style: {
                    fontSize: '16px',
                }
            },
        }],
        plotOptions: {
            column: {
                minPointLength: 3
            }
        }
    });
}


function learningCurve(dataset) {
    var data = $.map(dataset.tests, function(item, index) {
        var correct_answers_percentage = (item.correct_answers / item.apparatus.exercises_amount) * 100
        var allotted_time = getSeconds(item.apparatus.allotted_time) / item.apparatus.exercises_amount
        var exercises = $.map(item.exercises, function(exercise) {
            return [[exercise, correct_answers_percentage, allotted_time]]
        })
        var result = exercises.filter(exercise => {
            return exercise[0].answer_is_correct === true
        })
        return result;
    });
    var newData = data.map(function(item, index) {
        return [index+1, item[0].time_spent, item[1], item[2]]
    })
    Highcharts.chart('myChart3', {

        chart: {
            zoomType: 'x'
        },
        rangeSelector: {
            selected: 1
        },
        legend: {
            enabled: false
        },
        exporting: { enabled: false },
        title: {
            text: "Кривая обучения (по заданиям)",
        },
        colors: [
            'rgba(199, 35, 35, 0.6)',
        ],

        series: [{
            type: 'spline',
            name: 'Индекс освоения',
            data: newData.map(function(item) {
                if (getSeconds(item[1])/item[3] < 1) {
                    var speed_factor = 1
                }
                else {
                    var speed_factor = getSeconds(item[1])/item[3]
                }
                return item[1] = 1/speed_factor * item[2]
            }),
            tooltip: {
                valueDecimals: 2
            }
        }],
        yAxis: [{
            labels: {
                formatter: function() {
//                    return (this.value+'').toHHMMSS()
                    return this.value
                }
            },
            title: {
                text: 'Индекс освоения',
                style: {
                    fontSize: '16px',
                }
            },
            max: 100,
        }],
        xAxis: [{
            allowDecimals: false,
            title: {
                text: 'Успешно решенные примеры',
                style: {
                    fontSize: '16px',
                }
            },
        }],
        plotOptions: {
            column: {
                minPointLength: 3
            }
        }
    });
}


function learningCurveTests(dataset) {
    var data = $.map(dataset.tests, function(item, index) {
        var correct_answers_percentage = (item.correct_answers / item.apparatus.exercises_amount) * 100
        var time_spent = getSeconds(item.time_spent)
        var allotted_time = getSeconds(item.apparatus.allotted_time)
//        if (correct_answers_percentage == 100) {
//            var speed_factor =
//        }
        return [[index +1 , correct_answers_percentage]]
    });
//    var data = $.map(dataset.tests, function(item, index) {
//        var correct_answers_percentage = (item.correct_answers / item.apparatus.exercises_amount) * 100
//        var allotted_time = getSeconds(item.apparatus.allotted_time) / item.apparatus.exercises_amount
//        var exercises = $.map(item.exercises, function(exercise) {
//            return [[exercise, correct_answers_percentage, allotted_time]]
//        })
//        var result = exercises.filter(exercise => {
//            return exercise[0].answer_is_correct === true
//        })
//        return result;
//    });
    Highcharts.chart('myChart4', {

        chart: {
            zoomType: 'x'
        },
        rangeSelector: {
            selected: 1
        },
        legend: {
            enabled: false
        },
        exporting: { enabled: false },
        title: {
            text: "Кривая обучения (по тестам)",
        },
        colors: [
            'rgba(35, 35, 199, 0.9)',
        ],

        series: [{
            type: 'spline',
            name: 'Индекс освоения',
            data: data,
            tooltip: {
                valueDecimals: 2
            }
        }],
        yAxis: [{
            labels: {
                formatter: function() {
                    return this.value
                }
            },
            title: {
                text: 'Индекс освоения',
                style: {
                    fontSize: '16px',
                }
            },
        }],
        xAxis: [{
            allowDecimals: false,
            title: {
                text: 'Завершенные тесты',
                style: {
                    fontSize: '16px',
                }
            },
        }],
        plotOptions: {
            column: {
                minPointLength: 3,
            }
        }
    });
}


$(document).on('change', '#apparatus-selector', function (e) {
    //$('#description-value').html($(this).find('option:selected').data('description'))
    getDataset()
});

$(document).ready(function() {
    //$('#description-value').html($('#apparatus-selector').find('option:selected').data('description'))
    getDataset()
});