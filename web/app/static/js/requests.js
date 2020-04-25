$(document).ready(function(){

    $("#login_form").on("submit", function(event){
        $.ajax({
            data: {
                username : $('#username_login').val(),
                password : $('#password_login').val()
            },
            type : 'POST',
            url : '/login',
            datatype : 'json'
        }).done(function(data) {
                if(data.error){
                    console.log("Error : " + data.error)
                    $('#error_alert').text(data.error).show();
                    $('#success_alert').hide();
                }else{
                    if(data.results == "Username or password incorrect!"){
                        console.log("Error : " + data.results)
                        $('#error_alert').text(data.results).show();
                        $('#success_alert').hide(); 
                    }else{
                        console.log("Success! : " + data.results)
                        window.location.replace("http://sciq-unimib-dev.herokuapp.com/logged_user")
                    }
                }
            })
            .fail(function(err) {
                console.log("General error"+ err);
            });
    });
});