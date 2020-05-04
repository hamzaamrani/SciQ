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
                headers: {
                    Authorization: 'Bearer ' + localStorage.getItem('access_token')
                },
                data: JSON.stringify({'symbolic_expression': expression}),
                contentType: 'application/json;charset=UTF-8',
                success:function(response){ 
                    document.write(response); 
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
