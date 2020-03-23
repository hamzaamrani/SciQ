import pytest
from config import ConfigTest
from server import create_app
from server.database import db

@pytest.fixture
def app():
    app = create_app()
    app.config.from_object(ConfigTest)
    with app.app_context():   
        db.create_all()
        yield app
        # teardown
        db.session.remove()
        db.drop_all()