$(document).ready(function(){

    $("#login_form").bind("submit", function(event){
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
                    }
                }
            })
            .fail(function(err) {
                console.log("General error"+ err);
            });
            event.preventDefault()
    });
});