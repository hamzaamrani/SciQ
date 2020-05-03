$(document).ready(function(){
    


    // On search-button click
    $("#search-button").on("click", function(event){
        event.preventDefault();
        var expression = $('#symbolic_expression').val();
        console.log("expression " + expression);

        if(expression != ""){
            $.ajax({
                type : "POST",
                url : '/submit_expression',
                //contentType: 'application/json;charset=UTF-8',
                headers: {
                    Authorization: 'Bearer ' + localStorage.getItem('access_token')
                },
                data: "symbolic_expression=" + expression,
                contentType: 'application/x-www-form-urlencoded',
                success: function(data) {
                    if(data.error){
                        if (data.error === 'reached limit requests'){
                            console.log("Error : " + data.error)
                            $('#error_alert').text('reach limit requests for a not logged user (2 per hour)').show();
                        }
                    }else{
                        console.log("Success! : " + data.query)
                        console.log("Token: " + data.response_obj)
                    }
                },
                error: function(err) {
                console.error('General error: ' + err)
                }
            });

        }else{
            $('#error_alert').text("Empty expression. Please insert in input area").show();
        }
    });
})
