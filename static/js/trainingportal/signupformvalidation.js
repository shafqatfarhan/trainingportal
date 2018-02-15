
var submitButton = document.getElementById("submitBtn");
submitButton.addEventListener("click", validateform);

function validateform(event)
{
    var formObj = document.getElementById("signupForm");
    var first_name = formObj["first_name"].value;
    var last_name = formObj["last_name"].value;
    var username = formObj["username"].value;
    var email = formObj["email"].value;
    var password = formObj["password"].value;
    var designation = formObj["designation"].value;

    var error_text = "";

    if (first_name==null || first_name=="")
    {
        error_text += "(*) First name is required<br/>";
    }
    if (last_name==null || last_name=="")
    {
        error_text += "(*) Last name is required<br/>";
    }
    if(username==null || username=="")
    {
        error_text += "(*) Username is required<br/>";
    }
    if(email==null || email=="")
    {
        error_text += "(*) Email is required<br/>";
    }
    if(password==null || password=="")
    {
        error_text += "(*) Password is required<br/>";
    }
     if(designation==null || designation=="")
    {
        error_text += "(*) Designation is required<br/>";
    }

    if (error_text)
    {
        document.getElementById("validate_text").innerHTML = error_text;
        event.preventDefault();
    }

}
