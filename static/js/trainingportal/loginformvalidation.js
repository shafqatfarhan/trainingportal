/**
 * Created by shafaqat on 2/14/18.
 */
$(document).ready(function () {

    $('#error_msg').hide();
    $("#submitBtn").click(function(event) {
        var username = $("#id_username").val();
        var password = $("#id_password").val();
        if (username == null || username == '' ||
            password == null || password == '')
        {
            $('#validate_text').html('Username or password is empty<br/>');
            event.preventDefault();
        }
    });

    var frm = $('#loginForm');
        frm.submit(function () {
            $.ajax({
                type: frm.attr('method'),
                url: frm.attr('action'),
                data: frm.serialize(),
                success: function (data) {
                    data = JSON.parse(data);
                    if (data['failure_message'])
                    {$('#error_msg').show(1000);}
                    else
                    {
                        window.location.href = data['redirect_path'];
                    }
                },
                error: function(data) {
                    $('#error_msg').show(1000);
                }
            });
            return false;
        });
});