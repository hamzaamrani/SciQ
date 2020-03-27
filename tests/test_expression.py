from app import db
from app.models.models import User, Expression

expression_template1 = {
            'expression': "x + 2 = 5",
            'expression_type': "equation",
            'solutions': "3",
            'step': " ",
            'plot': " ",
            'alternate_forms': " ",
            'execution_time': "1"
}


def test_create_expression(app):
    ex = Expression(**expression_template1)
    user = User(username="user1", password="password1", token="token1")
    user.expressions.append(ex)
    db.session.add(user)
    db.session.add(ex)
    db.session.commit()
    expressions = Expression.query.all()
    assert len(expressions) == 1