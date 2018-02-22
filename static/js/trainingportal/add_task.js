/**
 * Created by shafaqat on 2/21/18.
 */

$(document).ready(function () {

    $("#submitBtn").click(function (event) {
        $('#validate_text').html('');
        var title = $("#id_title").val();
        var description = $("#id_description").val();

        if (title == null || title == '' ||
            description == null || description == '') {
            $('#validate_text').html('Required fields are empty.<br/>');
            event.preventDefault();
        }
    });

    var frm = $('#taskForm');
    frm.submit(function (event) {
        event.preventDefault();
        $('#validate_text').html('');
        var data = new FormData(frm.get(0));
        $.ajax({
            type: frm.attr('method'),
            url: frm.attr('action'),
            data: frm.serialize(),
            success: function (data) {
                data = JSON.parse(data);
                if (data['failure_message']) {
                    $('#validate_text').html('Required fields are empty.<br/>');
                }
                else {
                    frm.find("input, textarea").val("");
                    var modal = document.getElementById('myModal');
                    modal.style.display = "none";
                    alert('Task added successfully');
                    window.location.href = '/tasks/?trainer_id=' + data['trainer_id']
                    + '&training_id=' + data['training_id']
                    + '&trainee_id=' + data['trainee_id']
                }
            },
            error: function (data) {
                $('#validate_text').html('Required fields are empty.<br/>');
            }
        });
        return false;
    });
});