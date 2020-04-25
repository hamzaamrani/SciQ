$(document).ready(function(){
    


    // On login click
    $("#submit_login").on("click", function(event){
        event.preventDefault();
        var username = $('#username_login').val();
        var password = $('#password_login').val();
        console.log("username = " + username + " and password = " + password);

        if(username != "" && password != ""){
            $.ajax({
                type : "POST",
                url : '/login',
                contentType: 'application/json;charset=UTF-8',
                data: JSON.stringify({'username' : username, 'password' : password }),
                dataType: "json",
                success: function(data) {
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
                },
                error: function(err) {
                console.log("General error"+ err);
                }
            });

        }else{
            $('#error_alert').text("Username or password empty!").show();
            $('#success_alert').hide(); 
        }
    });

    // On signup click
    $("#submit_signup").on("click", function(event){
        event.preventDefault();
        var username = $('#username_signup').val();
        var pass1 = $('#password_signup1').val();
        var pass2 = $('#password_signup2').val();
        if(username != "" && pass1 != "" && pass2!= ""){
            if(pass1 == pass2){
                $.ajax({
                    type : "POST",
                    url : '/signup',
                    contentType: 'application/json;charset=UTF-8',
                    data: JSON.stringify({'username' : username, 'password1' : pass1, 'password2' : pass2}),
                    dataType: "json",
                    success: function(data) {
                        if(data.error){
                            console.log("Error : " + data.error)
                            $('#error_alert').text(data.error).show();
                            $('#success_alert').hide();
                        }else{
                            console.log("Success! : " + data.results)
                            $('#success_alert').text(data.results).show();
                            $('#error_alert').hide();
                        }
                    },
                    error: function(err) {
                    console.log("General error"+ err);
                    }
                });

            }else{
                $('#error_alert').text("Passwords must be equals!").show();
                $('#success_alert').hide(); 
            }
        }else{
            $('#error_alert').text("Username or password empty!").show();
            $('#success_alert').hide(); 
        }
        
    })



});