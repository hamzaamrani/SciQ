$(document).ready(function(){

    $("#login_form").on("submit", function(event){
        $.ajax({
            data: {
                username : $('#username_login').val(),
                password : $('#password_login').val()
            },
            method : "POST",
            url : '/login',
            success: function(data) {
                if(data.error){
                    $('#error_alert').text(data.error).show();
                    $('#success_alert').hide();
                }else{
                    if(data.results == "Username or password incorrect!"){
                        $('#error_alert').text(data.results).show();
                        $('#success_alert').hide(); 
                    }else{
                        window.location.href = "logged_user.html";
                    }
                }
            },
            error: function(err) {
                console.log(err);
            }
        });
    });
});