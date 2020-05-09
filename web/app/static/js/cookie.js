function getCookie(cname) {
var name = cname + "=";
    var decodedCookie = decodeURIComponent(document.cookie);
    var ca = decodedCookie.split(';');
    for(var i = 0; i <ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0) == ' ') {
        c = c.substring(1);
        }
        if (c.indexOf(name) == 0) {
        return c.substring(name.length, c.length);
        }
}
return "";
}

function checkCookie(){
    cookie = getCookie('access_token_cookie');
    console.log("Valore cookie: " + cookie);
    if (cookie == "") {
        $('#li_logout').hide(); 
        $('#li_developer').hide();
    }
    else{
        $('#li_logout').show(); 
        $('#li_developer').show();
    }
}
