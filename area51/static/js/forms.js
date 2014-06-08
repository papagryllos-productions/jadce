$(document).ready(function() {
  // For the red buttons that clear the form
  $("#clear").click(function() {
    $(this).closest("form").find("input[type=text], textarea").val("");
  });

  // this is to prevent sending empty forms
  $("#submitting").click(function() {
    if ($("#username").val() == '') {
      $(".error").hide();
      $("#username").after('<span class="error">You need to give at least a username.</span>');
      return false;
    }
    return true;
  });

  // For checking validity of the two password forms & the email
  $("#password2").keyup(matching_passwords);
  $("#email").keyup(validate_email);
});

function matching_passwords() {
  // we hide any previous stuff
  $(".error").hide();

  var passwordVal = $("#password1").val();
  var checkVal    = $("#password2").val();

  if (passwordVal == '') {
    $("#password1").after('<span class="error"><i class="fa fa-times"></i> Please enter a password.</span>');
    return false;
  } else if (checkVal == '') {
    $("#password2").after('<span class="error"><i class="fa fa-times"></i> Please confirm your password.</span>');
    return false;
  } else if (passwordVal != checkVal) {
    $("#password2").after('<span class="error"><i class="fa fa-times"></i> Passwords do not match.</span>');
    return false;
  } else if (passwordVal == checkVal) {
    $("#password2").after('<span class="error"><i class="fa fa-check"></i> Passwords match.</span>');
    return true;
  }
}

function validate_email() {
  $(".error").hide();

  var email = $("#email").val();
  var re = /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;

  if (re.test(email)) {
    $("#email").after('<span class="error"><i class="fa fa-check"></i> Email is valid.</span>');
    return true;
  } else {
    $("#email").after('<span class="error"><i class="fa fa-times"></i> Please enter a valid email.</span>');
    return false;
  }
}
