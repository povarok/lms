function createControlTest(obj) {
    var selectedApparatus = obj.name;
    var data = {
    testType: 'control',
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
function controlTestPopup(test) {
  test = test.replace(/"/g, '\\"')
  test = test.replace(/None/g, '"none"')
  test = test.replace(/True/g, '"true"')
  test = test.replace(/False/g, '"false"')
  test = test.replace(/'/g, '"')
  obj = JSON.parse(test)
  obj.description = obj.description.replace(/\\/g, '')
  function kek() {if (obj.control_tests.length) { return 'Пройти тест еще раз' } else { return 'Начать контрольный тест' }};
  Swal.fire({
    title: obj.name,
    html: obj.description,
    width: "600px",
//    showCancelButton: true,
//    cancelButtonColor: '#d33',
    confirmButtonText: kek(),
//    allowOutsideClick: false,
//    cancelButtonText: 'Отменить',
  })
  .then(
    result => {
    if (result.value) {
      createControlTest(obj);
    } else {
    }
  }
)}
