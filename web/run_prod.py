from flask_migrate import MigrateCommand
from flask_script import Manager

from web.app import create_app

from os import environ


if environ.get('STEP') == 'staging':
    app = create_app("pre_prod")
else: 
    app = create_app("production")

manager = Manager(app)
manager.add_command("db", MigrateCommand)

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=False)
