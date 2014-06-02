$("#send").click(function() {
  $.ajax({
    type: "POST",
    url: '/api/adduser',
    data: $(this).closest("form").serialize(),
    success: function() {
      window.history.back()
    },
    failure: function() {
      alert("Something went wrong! Try again.");
    }
  });
});

$("#log").click(function() {
  $.ajax({
    type: "POST",
    url: '/api/login',
    data: $(this).closest("form").serialize(),
    success: function() {
      window.history.back()
    },
    failure: function() {
      alert("Something went wrong! Try again.");
    }
  });
});

$("#clear").click(function() {
    $(this).closest("form").find("input[type=text], textarea").val("");
});
