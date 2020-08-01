$(function () {
    // Materializecss widget init
    $('.tooltipped').tooltip();

    // Populate Students List table
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
                    if (text == 'expired') {
                        tr.append("<td class='red-text'>" + text + "</td>");
                    } else if (text == 'active') {
                        tr.append("<td class='green-text'>" + text + "</td>");
                    } else if (text == 'probation') {
                        tr.append("<td class='orange-text'>" + text + "</td>");
                    } else {
                        tr.append("<td>" + text + "</td>");
                    }
                });
                tr.appendTo(tbody);
            });

            // Search term control
            $("#search_term").keyup(function () {
                $("#all-students-list tbody tr").remove();
                var searchTerm = $("#search_term").val();
                eel.getFilteredStudentResult(searchTerm)(function (students) {
                    const tbody = $("#all-students-list tbody");
                    var data = JSON.parse(students);
                    let tr = $("<tr />");
                    $.each(data, function (_, obj) {
                        tr = $("<tr />");
                        $.each(obj, function (_, text) {
                            if (text == 'expired') {
                                tr.append("<td class='red-text'>" + text + "</td>");
                            } else if (text == 'active') {
                                tr.append("<td class='green-text'>" + text + "</td>");
                            } else if (text == 'probation') {
                                tr.append("<td class='orange-text'>" + text + "</td>");
                            } else {
                                tr.append("<td>" + text + "</td>");
                            }
                        });
                        tr.appendTo(tbody);
                    });
                });
            });
        });
    });
});