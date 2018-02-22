/**
 * Created by shafaqat on 2/22/18.
 */

$(document).ready(function () {

    var submitAssignmentForm = $('#submitAssignmentForm');
    submitAssignmentForm.submit(function (event) {
        event.preventDefault();
        var data = new FormData(submitAssignmentForm.get(0));
        $.ajax({
            type: submitAssignmentForm.attr('method'),
            url: submitAssignmentForm.attr('action'),
            processData: false,
            contentType: false,
            data: data,
            success: function (data) {
                data = JSON.parse(data);
                if (data['failure_message']) {
                    alert('File not uploaded.');
                }
                else {
                    submitAssignmentForm.find("input, textarea").val("");
                    alert('Assignment Submitted successfully');
                    window.location.href = data['redirect_path']
                }
            },
            error: function (data) {
                alert('Required field(s) are empty');
            }
        });
        return false;
    });
});

