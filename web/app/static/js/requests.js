$(document).ready(function(){

    $("#login_form").on("submit", function(event){

        $.ajax({
            data: {
                username : $('#username_login').val(),
                password : $('#password_login').val()
            },
            type : 'POST',
            url : '/login'
        }).done(function(data){
            console.log(data)
            if(data.error){
                $('#error_alert').text(data.error).show();
                $('#success_alert').hide();
            }else{
                $('#success_alert').text(data.results).show();
                $('#error_alert').hide();
                window.location.href = "logged_user.html";
            }
        })

        event.preventDefault();
    });

});