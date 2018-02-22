/**
 * Created by shafaqat on 2/16/18.
 */

$(document).ready(function () {

    $("#submitBtn").click(function (event) {
        $('#validate_text').html('');
        var title = $("#id_title").val();
        var description = $("#id_description").val();
        var due_date = $("#id_due_date").val();

        if (title == null || title == '' ||
            description == null || description == '' ||
            due_date == null || due_date == '') {
            $('#validate_text').html('Required fields are empty.<br/>');
            event.preventDefault();
        }
    });

    var frm = $('#trainingForm');
    frm.submit(function (event) {
        event.preventDefault();
        $('#validate_text').html('');
        var data = new FormData(frm.get(0));
        $.ajax({
            type: frm.attr('method'),
            processData: false,
            contentType: false,
            url: frm.attr('action'),
            data: data,
            success: function (data) {
                data = JSON.parse(data);
                if (data['failure_message']) {
                    $('#validate_text').html('Required fields are empty.<br/>');
                }
                else {
                    frm.find("input, textarea").val("");
                    var modal = document.getElementById('myModal');
                    modal.style.display = "none";
                    alert('Training added successfully');
                    window.location.href = frm.attr('action');
                }
            },
            error: function (data) {
                $('#validate_text').html('Required fields are empty.<br/>');
            }
        });
        return false;
    });

    var edit_form = $('#editTrainingForm');
    edit_form.submit(function (event) {
        event.preventDefault();
        $('#validate_text').html('');
        var data = new FormData(edit_form.get(0));
        $.ajax({
            type: edit_form.attr('method'),
            processData: false,
            contentType: false,
            url: edit_form.attr('action'),
            data: data,
            success: function (data) {
                data = JSON.parse(data);
                if (data['failure_message']) {
                    $('#validate_text').html('Required fields are empty.<br/>');
                }
                else {
                    edit_form.find("input, textarea").val("");
                    alert('Training edited successfully.');
                    window.location.href = data['redirect_path'];
                }
            },
            error: function (data) {
                $('#validate_text').html('Required fields are empty.<br/>');
            }
        });
        return false;
    });

    $(function () {
        $.ajaxSetup({
            headers: {"X-CSRFToken": getCookie("csrftoken")}
        });
    });
});


function delete_training(training_id) {
    if (confirm("Are you sure you want to delete training?")) {
        $(document).ready(function () {
            $.ajax({
                type: 'DELETE',
                url: '/delete_training/',
                data: {
                    'training_id': training_id
                },
                success: function (data) {
                    data = JSON.parse(data);
                    if (data['success_message']) {
                        alert(data['success_message']);
                        window.location.href = data['redirect_path'];
                    }
                },
                error: function (data) {
                    alert("Failed to delete training.");
                }
            });
        });
    }
}

function getCookie(c_name) {
    if (document.cookie.length > 0) {
        c_start = document.cookie.indexOf(c_name + "=");
        if (c_start != -1) {
            c_start = c_start + c_name.length + 1;
            c_end = document.cookie.indexOf(";", c_start);
            if (c_end == -1) c_end = document.cookie.length;
            return unescape(document.cookie.substring(c_start, c_end));
        }
    }
    return "";
}

