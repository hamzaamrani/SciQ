from app import db
from . import expression_blueprint
from flask import request, jsonify
from app.models import Expression, ExpressionSchema, User, user_expression

expression_schema = ExpressionSchema()
expressions_schema = ExpressionSchema(many=True)

# create expression for a user
@expression_blueprint.route('/', methods=['POST'])
def create_expression():
    username = request.json['username']
    expression = request.json['expression']
    solutions = request.json['solutions']

    user = User.query.filter_by(username=username).first()

    ex = Expression.query.filter_by(expression=expression).first()

    # check if there is yet expression
    if ex is None:
        ex = Expression(expression=expression,
                        solutions=solutions)

    # check if user added yet this expression
    if ex not in user.expressions:

        user.expressions.append(ex)  
        db.session.add(user)
        db.session.commit()

        return expression_schema.jsonify(ex)

    else:

        return jsonify({'error': 'hai già aggiunto questa espressione'})

# get all expressions of a user
@expression_blueprint.route('/<username>', methods=['GET'])
def get_ex_user(username):
    ex = User.query.filter_by(username=username).first().expressions
    ex = expressions_schema.dump(ex)
    return jsonify(ex)

# delete an expression of a user
@expression_blueprint.route('/<username>', methods=['DELETE'])
def delete_ex_for_user(username):
    expression = Expression.query.filter_by(expression=request.json['expression']).first()
    user = User.query.filter_by(username=username).first()
    user.expressions.remove(expression)
    db.session.commit()

    return expression_schema.jsonify(expression)