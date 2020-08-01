$(function () {
    $.get('student-list.html', function (response) {
        $('.div-container-student-list').html(response);

        // Gets the all students on load
        eel.getAllStudents()(function (students) {
            const tbody = $("#all-students-list tbody");
            var data = JSON.parse(students);
            let tr = $("<tr />");
            $.each(data, function (_, obj) {
                tr = $("<tr />");
                $.each(obj, function (_, text) {
                    tr.append("<td>" + text + "</td>")
                });
                tr.appendTo(tbody);
            });
        });
    });

    $('.tooltipped').tooltip();
})