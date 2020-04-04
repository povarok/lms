function createTest() {
    var selector = document.getElementById("apparatus-selector");
    var selectedApparatus = selector.options[selector.selectedIndex].text;
    var data = {
    trainingApparatus: selectedApparatus,
    timeStart: new Date(),
    }
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

$(document).on('change', '#apparatus-selector', function (e) {
    $('#description-value').html($(this).find('option:selected').data('description'))
});

$(document).ready(function() {
    $('#description-value').html($('#apparatus-selector').find('option:selected').data('description'))
});