$(function () {
    eel.getNewUserStatus()(function (s) {
        var status = s
        if (status == "1") {
            var URL = "index.html"
            setTimeout(
                function () {
                    window.location.replace(URL);
                },
                3000
            );
        } else {
            var URL = "adminsignin.html"
            setTimeout(
                function () {
                    window.location.replace(URL);
                },
                3000
            );
        }
    });
});