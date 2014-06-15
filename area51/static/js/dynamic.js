/* Function for dynamically requesting data and displaying them */
function updateData() {
  $.get('/api/data', function(data) {
    $('#dynamic').html(data);
  });
}
setInterval('updateData()', 1000);

/* Adding the extra attribute to the image upload buttons. Freaking django. */
$('#id_photo1').attr('accept', 'image/*;capture=camera');
$('#id_photo2').attr('accept', 'image/*;capture=camera');
$('#id_photo3').attr('accept', 'image/*;capture=camera');
$('#id_photo4').attr('accept', 'image/*;capture=camera');
