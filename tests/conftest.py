import pytest
from server import create_app, db

@pytest.fixture
def app():
    app = create_app('testing')
    with app.app_context():   
        db.create_all()
        yield app
        # teardown
        db.session.remove()
        db.drop_all()