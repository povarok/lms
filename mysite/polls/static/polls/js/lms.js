function createTest() {
    var data = {
    trainingApparatus: 1,
    timeStart: new Date(),
    }
    console.log('data', data)
    $.ajax({
        method: 'POST',
        url: '/api_create_test/',
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
            window.location.href='/primer';
        }
    }).fail(function (err) {
        console.log(`[AJAX] error `, err);
    });
}
$(document).on('click', '#button-got-it', createTest)