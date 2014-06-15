/* Code to actually locate the user and initialize the map */
var options = {
  enableHighAccuracy: true,
  timeout: 5000,
  maximumAge: 0
};

function successy(pos) {
  var crd = pos.coords;

  /* we are dynamically adding the coordinates to the input fields of the widget */
  $('#id_position_0').val(crd.latitude);
  $('#id_position_1').val(crd.longitude);

  /* triggering keyup event for the widget to update itself */
  var e = jQuery.Event('keyup');
  e.which = 20;
  e.ctrlKey = false;
  e.keyCode = 20;
  $('#id_position_0').trigger(e);
}

function errory(err) {
  console.warn('ERROR(' + err.code + '): ' + err.message);
}

/* let the magic happen */
navigator.geolocation.getCurrentPosition(successy, errory, options);
