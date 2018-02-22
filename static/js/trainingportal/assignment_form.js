/**
 * Created by shafaqat on 2/22/18.
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

    var frm = $('#assignmentForm');
    frm.submit(function (event) {
        event.preventDefault();
        $('#validate_text').html('');
        var data = new FormData(frm.get(0));
        $.ajax({
            type: frm.attr('method'),
            url: frm.attr('action'),
            processData: false,
            contentType: false,
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
                    alert('Assignment added successfully');
                    window.location.href = '/assignments/?task_id=' + data['task_id']
                }
            },
            error: function (data) {
                $('#validate_text').html('Required fields are empty.<br/>');
            }
        });
        return false;
    });

    $("#evaluateBtn").click(function (event) {
        $('#validate_text').html('');
        var score = $("#id_score").val();
        var remarks = $("#id_remarks").val();

        if (score == null || score == '' ||
            remarks == null || remarks == '') {
            $('#validate_text').html('Required fields are empty.<br/>');
            event.preventDefault();
        }
    });

    var evaluateForm = $('#evaluateAssignmentForm');
    evaluateForm.submit(function (event) {
        event.preventDefault();
        $('#validate_text').html('');
        var data = new FormData(evaluateForm.get(0));
        $.ajax({
            type: evaluateForm.attr('method'),
            url: evaluateForm.attr('action'),
            processData: false,
            contentType: false,
            data: data,
            success: function (data) {
                data = JSON.parse(data);
                if (data['failure_message']) {
                    $('#validate_text').html('Required fields are empty.<br/>');
                }
                else {
                    evaluateForm.find("input, textarea").val("");
                    alert('Assignment Evaluated successfully');
                    window.location.href = data['redirect_path']
                }
            },
            error: function (data) {
                $('#validate_text').html('Required fields are empty.<br/>');
            }
        });
        return false;
    });
});
