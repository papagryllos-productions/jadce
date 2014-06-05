$(document).ready(function() {
  // For the red buttons that clear the form
  $("#clear").click(function() {
    $(this).closest("form").find("input[type=text], textarea").val("");
  });
});
