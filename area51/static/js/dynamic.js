function updateData() {
  $.get('/api/data', function(data) {
    $('#dynamic').html(data);
  });
}

setInterval("updateData()", 1000);
