from flask import Blueprint

user_blueprint = Blueprint('user', __name__, url_prefix='/user')
expression_blueprint = Blueprint('expression', __name__, url_prefix='/expression')

from . import user, expression