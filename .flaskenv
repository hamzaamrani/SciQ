FLASK_APP=wsgi.py
SECRET_KEY='chiave_segreta'
TESTING=True
FLASK_ENV='development' 
DEBUG=True
SQLALCHEMY_TRACK_MODIFICATIONS=False
DATABASE_URI_DEV="sqlite:///db\db.sqlite"
DATABASE_URI_TEST="sqlite:///db\test.sqlite"