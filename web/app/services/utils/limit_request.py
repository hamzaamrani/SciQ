from flask import current_app as app
from flask import request
import jwt  
import logging

from web.app.models import User
from web.app import limiter, LIMIT

logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.DEBUG)

def get_user_type(request):
    """
    Check if ther's a token in the request and that is valid, with a 
    username registered in the system
    """

    if request.is_json:
        _json = request.json
        if 'access_token' in _json:
            decode = jwt.decode(_json['access_token'].encode(), app.config['SECRET_KEY'], algorithms=['HS512'])
            logging.info("Token ricevuto da client {}".format(decode))
            if User.query.filter_by(username=decode['sub']).first():
                logging.info("sono unlimited")
                return True
            else:
                logging.info("token non valido")
                return False
        else:
            logging.info("sono limited")
            return False
    else:
        auth_header = request.headers.get('Authorization')
        if auth_header:
            try:
                auth_token = auth_header.split(' ')[1]
                decode = jwt.decode(auth_token.encode(), app.config['SECRET_KEY'], algorithms=['HS512'])
                logging.info("Token ricevuto da client {}".format(decode))
                if User.query.filter_by(username=decode['sub']).first():
                    logging.info("sono unlimited")
                    return True
                else:
                    logging.info("token non valido")
                    return False
            except IndexError:
                return False
        else:
            return False