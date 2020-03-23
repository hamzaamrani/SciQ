from flask import Blueprint

user_blueprint = Blueprint('user', __name__)
expression_blueprint = Blueprint('expression', __name__)

from . import user, expression