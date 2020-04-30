from functools import wraps
from flask import current_app as app
from flask import request
import jwt  
import logging

from web.app.models import User
from web.app import limiter, LIMIT

logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.DEBUG)
'''
def rate_limited_resource():
    """
    Rate limit a resource depending on the user
    """
    def wrapper(f):
        logged_user = limiter.exempt(f)  
        not_logged_user = limiter.limit(LIMIT)(f)

        @wraps(f)
        def decorated(*args, **kwargs):
            logged = get_user_type(request)

            if logged=='unlimited':
                return logged_user(*args, **kwargs)
            elif logged=='limited':
                return not_logged_user(*args, **kwargs)
        return decorated
    return wrapper
'''
def get_user_type(request):
    """
    Check if ther's a token in the request and that is valid, with a 
    username registered in the system
    """

    if request.is_json:
        _json = request.json
        # check if ther's a token
        if 'token' in _json:
            decode = jwt.decode(_json['token'].encode(), app.config['SECRET_KEY'], algorithms=['HS512'])
            logging.info(decode)
            #if User.query.filter_by(username=decode.username).first():
            if decode['username'] == 'prova_logged':
                logging.info("sono unlimited")
                return True
            else:
                logging.info("token non valido")
                return {'error': 'token not valid, try to re-login'}
        else:
            logging.info("sono limited")
            return False
    else:
        logging.info("richiesta mal formata")
        return {'error': 'malformed request, must be a JSON with a token'}