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
    if (cookie == "") {
        $('#li_logout').hide(); 
        $('#li_developer').hide();
    }
    else{
        $('#li_logout').show(); 
        $('#li_developer').show();
    }
}

function readCookie(name) {
    var nameEQ = name + "=";
    var ca = document.cookie.split(';');
    for (var i = 0; i < ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0) == ' ') c = c.substring(1, c.length);
        if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length, c.length);
    }
    return null;
}
var cookieRegistry = [];

function listenCookieChange(cookieName, callback) {
    setInterval(function() {
        if (cookieRegistry[cookieName]) {
            if (readCookie(cookieName) === null) {
                // update registry so we dont get triggered again
                cookieRegistry[cookieName] = readCookie(cookieName);
                return callback();
            }
        } else {
            cookieRegistry[cookieName] = readCookie(cookieName);
        }
    }, 100);
}

// bind the listener
listenCookieChange('access_token_cookie', function() {
    alert('session expired, you will redirect to login page');
    setTimeout(function () {
        window.location = '/'
    }, 200);
});
