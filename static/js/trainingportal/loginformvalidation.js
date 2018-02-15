/**
 * Created by shafaqat on 2/14/18.
 */
$(document).ready(function () {

    $("#submitBtn").click(function(event) {
        var username = $("#id_username").val();
        var password = $("#id_password").val();
        if (username == null || username == '' ||
            password == null || password == '')
        {
            $('#validate_text').html('Username or password is empty<br/>');
            event.preventDefault();
        }
        else
        {

        }
    });

    var frm = $('#loginForm');
        frm.submit(function () {
            $.ajax({
                type: frm.attr('method'),
                url: frm.attr('action'),
                data: frm.serialize(),
                success: function (data) {
                    alert(data);
                    $('html').html(data);
                },
                error: function(data) {
                    alert('Request failed.');
                }
            });
            return false;
        });
});