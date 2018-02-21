/**
 * Created by shafaqat on 2/21/18.
 */

function update_training_status(training_id) {
    $(document).ready(function () {
        $.ajax({
            type: 'POST',
            url: '/training_status/',
            data: {
                'training_id': training_id
            },
            success: function (data) {
                data = JSON.parse(data);
                if (data['success_message']) {
                        $('#' + training_id).attr('disabled', 'disabled');
                        $('#status_' + training_id).text('Completed');

                }
            },
            error: function (data) {
                alert("Failed to update training status.");
            }
        });
    });
}
