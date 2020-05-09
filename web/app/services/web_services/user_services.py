import mysql.connector
from flask import current_app
import logging
logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.DEBUG)

from web.app.config import DB_CONFIG_DEV, DB_CONFIG_PROD, DB_CONFIG_PRE_PROD

from os import environ

class UserService:
    def __init__(self):
        print("Connecting")

        if current_app.config["FLASK_ENV"] == "development":
            self.connection = mysql.connector.connect(**DB_CONFIG_DEV)
        else:
            if environ.get('STEP') == 'production':
                self.connection = mysql.connector.connect(**DB_CONFIG_PROD)
            else:
                self.connection = mysql.connector.connect(**DB_CONFIG_PRE_PROD)


    def check_exist(self, username):
        cursor = self.connection.cursor()
        query = f'SELECT * FROM user WHERE username="{username}"'
        cursor.execute(query)
        results = [user for user in cursor]
        cursor.close()
        return len(results) > 0

    def check_credentials(self, username, password, id=False):
        cursor = self.connection.cursor()
        query = f"SELECT * FROM user WHERE username='{username}' and password='{password}'"
        cursor.execute(query)
        results = [user for user in cursor]
        cursor.close()
        if id:
            if len(results)>0:
                id_user = results[0][0]
            else:
                id_user = 0
            return len(results) > 0, id_user
        else:
            return len(results) > 0

    def signup(self, username, password):
        cursor = self.connection.cursor()
        if self.check_exist(username):
            return False
        query = f'INSERT INTO user (username, password) VALUES ("{username}", "{password}")'
        cursor = self.connection.cursor()
        cursor.execute(query)
        self.connection.commit()
        cursor.close()
        return True
