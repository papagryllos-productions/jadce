/* Function for dynamically requesting data and displaying them */
function updateData() {
  $.get('/api/data', function(data) {
    $('#dynamic').html(data);
  });
}
setInterval("updateData()", 1000);

/* Adding the extra attribute to the image upload buttons. Freaking django. */
$('#id_photo').attr("accept", "image/*;capture=camera");
