import os
from server import create_app, db
from server.models.models import User, Expression
from flask_migrate import MigrateCommand
from flask_script import Manager, Shell

if os.environ.get('FLASK_ENV') == 'development':
    app = create_app('default')
elif os.environ.get('FLASK_ENV') == 'production':
    app = create_app('production')
    
manager = Manager(app)

def make_shell_context():
    return dict(app=app, db=db, User=User, Expression=Expression) 
 
manager.add_command("shell", Shell(make_context=make_shell_context))
 
if __name__ == '__main__':
    manager.run()