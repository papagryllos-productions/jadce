$(document).ready(function() {
    // For the red buttons that clear the form
    $('#clear').click(function() {
        $(this).closest('form').find('input[type=text], textarea').val('');
    });

    /*
     * These are to prevent sending empty forms
     */
    $('#submitting').click(function() {
        if ($('#username').val() == '') {
            $('.error').hide();
            $('.fine').hide();
            $('#username').after('<span class="error"><i class="fa fa-exclamation"></i> You need to give at least a username.</span>');
            return false;
        } else if ($('#password1').val() == '') {
            $('.error').hide();
            $('.fine').hide();
            $('#password1').after('<span class="error"><i class="fa fa-exclamation"></i> You need a password in order to log-in.</span>');
            return false;
        } else if ($('#password2').val() == '') {
            $('.error').hide();
            $('.fine').hide();
            $('#password2').after('<span class="error"><i class="fa fa-exclamation"></i> Please confirm your password.</span>');
            return false;
        } else {
            return true;
        }
    });

    $('#submitting-event').click(function() {
        if ($('#id_title').val() == '') {
            $('.error').hide();
            $('.fine').hide();
            $('#id_title').after('<span class="error"><i class="fa fa-exclamation"></i> You need to give a title.</span>');
            // jump to the top
            $('html, body').animate({ scrollTop: 0 }, 'fast');
            return false;
        }
        return true;
    });

    $('#new-cat-button').click(function() {
        if ($('#new-cat-field').val() == '') {
            return false;
        } else {
            return true;
        }
    });

    // For checking validity of the two password forms & the email
    $('#password2').keyup(matching_passwords);
    $('#email').keyup(validate_email);
    $('#username').keyup(username_availability);
});

function matching_passwords() {
    // we hide any previous stuff
    $('.error').hide();
    $('.fine').hide();

    var passwordVal = $('#password1').val();
    var checkVal = $('#password2').val();

    if (passwordVal == '') {
        $('#password1').after('<span class="error"><i class="fa fa-times"></i> Please enter a password.</span>');
        return false;
    } else if (checkVal == '') {
        $('#password2').after('<span class="error"><i class="fa fa-times"></i> Please confirm your password.</span>');
        return false;
    } else if (passwordVal != checkVal) {
        $('#password2').after('<span class="error"><i class="fa fa-times"></i> Passwords do not match.</span>');
        return false;
    } else if (passwordVal == checkVal) {
        $('#password2').after('<span class="fine"><i class="fa fa-check"></i> Passwords match.</span>');
        return true;
    }
}

function validate_email() {
    $('.error').hide();
    $('.fine').hide();

    var email = $('#email').val();
    var re = /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;

    if (re.test(email)) {
        $('#email').after('<span class="fine"><i class="fa fa-check"></i> Email is valid.</span>');
        return true;
    } else {
        $('#email').after('<span class="error"><i class="fa fa-times"></i> Please enter a valid email.</span>');
        return false;
    }
}

function username_availability() {
    $('.error').hide();
    $('.fine').hide();
    $.get('/api/user_list', function(data) {
        var usernames = data.split(',');
        if (containsObject($('#username').val(), usernames)) {
            $('#username').after('<span class="error"><i class="fa fa-times"></i> Username already exists.</span>');
            return false;
        } else {
            return true;
        }
    });
}

/* aux function to check if 'obj' inside 'list' array */
function containsObject(obj, list) {
    var i;
    for (i = 0; i < list.length; i++) {
        if (list[i] === obj) {
            return true;
        }
    }
    return false;
}
