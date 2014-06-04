//
// Area51 (jadce) form javascript code
// CSRF-secured post requests
//

// Some auxiliary function
function getCookie(name) {
  var cookieValue = null;
  if (document.cookie && document.cookie != '') {
    var cookies = document.cookie.split(';');
    for (var i = 0; i < cookies.length; i++) {
      var cookie = jQuery.trim(cookies[i]);
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) == (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

function csrfSafeMethod(method) {
  // these HTTP methods do not require CSRF protection
  return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

function sameOrigin(url) {
  // test that a given url is a same-origin URL
  // url could be relative or scheme relative or absolute
  var host = document.location.host; // host + port
  var protocol = document.location.protocol;
  var sr_origin = '//' + host;
  var origin = protocol + sr_origin;
  // Allow absolute or scheme relative URLs to same origin
  return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
    (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
    // or any other URL that isn't scheme relative or absolute i.e relative.
    !(/^(\/\/|http:|https:).*/.test(url));
}

//
// We get the csrf cookie and setting a handler so it will be sent on every POST req
//
var csrftoken = getCookie('csrftoken');

$.ajaxSetup({
  beforeSend: function(xhr, settings) {
    if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
      // Send the token to same-origin, relative URLs only.
      // Send the token only if the method warrants CSRF protection
      // Using the CSRFToken value acquired earlier
      xhr.setRequestHeader("X-CSRFToken", csrftoken);
    }
  }
});

$(document).ready(function() {
  $("#send").click(function() {
    $.ajax({
      type: "POST",
      url: '/api/adduser/',
      data: $(this).closest("form").serialize(),
      success: function(data, ret) {
        // We need this, so we would be able to redirect after the 'hidden'
        // POST request from the button.
        window.location.href = data;
      },
      failure: function(data, ret) {
        alert("Something went wrong! Try again.");
      }
    });
  });

  $("#log").click(function() {
    $.ajax({
      type: "POST",
      url: '/api/login/',
      data: $(this).closest("form").serialize(),
      success: function(data, ret) {
        window.location.href = data;
      },
      failure: function(data, ret) {
        alert("Something went wrong! Try again.");
      }
    });
  });

  // For the red buttons that clear the form
  $("#clear").click(function() {
    $(this).closest("form").find("input[type=text], textarea").val("");
  });
});
