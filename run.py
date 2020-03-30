from app import create_app, db
from flask_script import Manager

app = create_app('default')

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)