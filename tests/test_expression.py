from app import db
from app.models.models import User, Expression

expression_template1 = {
            'user_id'
            'expression',
            'expression_type',
            'solutions',
            'step',
            'plot',
            'alternate_forms',
            'execution_time'
}


def test_create_expression(app):
    user_created = Expression()
    users = User.query.all()
    assert len(users) == 1
    assert users[0].username == "test1"
    assert users[0].password == "password1"
