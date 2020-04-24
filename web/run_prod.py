#from flask_migrate import MigrateCommand
#from flask_script import Manager

from web.app import create_app

import os
from os import environ

# to del
print(os.getenv('STEP'))

'''
if environ.get('STEP') == 'staging':
    app = create_app("pre_prod")
else: 
    app = create_app("production")
'''   

if os.getenv('STEP') == 'staging':
    app = create_app("pre_prod")
else: 
    app = create_app("production")


print("URI database: ", app.config['SQLALCHEMY_DATABASE_URI'])

#manager = Manager(app)
#manager.add_command("db", MigrateCommand)

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=False)
