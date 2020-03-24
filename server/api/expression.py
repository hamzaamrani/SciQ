from server import db
from . import expression_blueprint
from .decorators import decorator
from flask import request, jsonify
from server.models.models import Expression, ExpressionSchema

expression_schema = ExpressionSchema()
expressions_schema = ExpressionSchema(many=True)

# create expression for a user
@expression_blueprint.route('/expression/<int:user_id>', methods=['POST'])
def create_expression(user_id):
    username = request.json['expression']
    password = request.json['result']
    step = request.json['step']
    expression = ExpressionSchema(expression=expression,
                                  result=result, step=step, user_id=user_id)
    db.session.add(expression)
    db.session.commit()
    return expression_schema.jsonify(expression)

# get all expressions of a user
@expression_blueprint.route('/expression/<int:user_id>', methods=['GET'])
def get_all_expression(user_id):
    expressions = Expression.query.get(user_id)
    result = expressions_schema.dump(expressions)
    return jsonify(result)

# delete an expression of a user
@expression_blueprint.route('/expression/<int:user_id>', methods=['DELETE'])
def delete_expression(user_id):
    user = User.query.get(user_id)
    db.session.delete(user)
    db.session.commit()
    return user_schema.jsonify(user)
