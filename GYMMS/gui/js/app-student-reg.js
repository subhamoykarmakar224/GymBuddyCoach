$(function () {
    // Widget init
    $('.timepicker').timepicker();
    $('.materialboxed').materialbox();
    $('.datepicker').datepicker({
        onOpen: function () {
            var instance = M.Datepicker.getInstance($('.datepicker'));
            instance.options.minDate = new Date();
            instance.options.firstDay = 1;
            instance.options.format = "dd mmmm, yyyy";
        }
    });
});

function readURL(input) {
    // alert(input.files[0].name);
    var fileName = input.files[0].name;
    var extn = fileName.substring(fileName.lastIndexOf('.') + 1).toLowerCase();
    if (extn == "gif" || extn == "png" || extn == "jpg" || extn == "jpeg") {
        if (input.files && input.files[0]) {
            var reader = new FileReader();

            reader.onload = function (e) {
                $('#blah').attr('src', e.target.result);
                eel.saveImage(e.target.result, input.files[0].name)(function () {
                    alert('saved');
                });
            };
            reader.readAsDataURL(input.files[0]);
        }
    } else {
        $('#blah').attr('src', './src/icons/ic_account_profile.png');
        alert("Error : Wrong Image Selected!");
    }
}