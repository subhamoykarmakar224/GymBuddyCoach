$(function () {
    $('.modal').modal();
    $("#phone_no").val("");
    $("#passwd").val("");
    $("#btnSignIn").on("click", function () {
        var phone = $("#phone_no").val();
        var passwd = $("#passwd").val();

        let isnum = /^\d+$/.test(phone);
        if (!isnum) {
            $("#error_msg").text("The phone number you have entered is invalid!");
            $('#modal-error').modal('open');
            return
        }

        if (phone.length != 10) {
            $("#error_msg").text("The phone number you have entered is not a valid phone number.");
            $('#modal-error').modal('open');
            return
        }

        if (passwd.length == 0) {
            $("#error_msg").text("The password field cannot be left blank.");
            $('#modal-error').modal('open');
            return;
        }

        // checkCredForLogin
        eel.checkCredForLogin(phone, passwd)(function (status) {
            if (status == 1) {
                var URL = "index.html"
                setTimeout(
                    function () {
                        window.location.replace(URL);
                    },
                    1
                );
            } else {
                $("#error_msg").text("Wrong phone number or password. Please try again.");
                $('#modal-error').modal('open');
                return;
            }
        });
    });

});