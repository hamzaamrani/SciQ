import logging
from os import environ

import mysql.connector
from flask import current_app
from web.app.config import DB_CONFIG_DEV, DB_CONFIG_PRE_PROD, DB_CONFIG_PROD

logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.DEBUG)


class UserService:
    def __init__(self):
        print("Connecting")

        if current_app.config["FLASK_ENV"] == "development":
            self.connection = mysql.connector.connect(**DB_CONFIG_DEV)
        else:
            if environ.get("STEP") == "production":
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
            if len(results) > 0:
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

    def check_appid(self, userid, appid):
        cursor = self.connection.cursor()
        query = f'select username_fk from application where appid="{appid}"'
        cursor.execute(query)
        results = [(userid, appid) for userid in cursor if userid]
        cursor.close()
        return results

    def add_application(self, userid, appid, appname):
        cursor = self.connection.cursor()
        query = f'INSERT INTO application (appid, username_fk, name) VALUES ("{appid}", "{userid}", "{appname}")'
        cursor.execute(query)
        self.connection.commit()
        cursor.close()
        return True

    def get_applications(self, userid):
        cursor = self.connection.cursor()
        query = (
            f'SELECT appid, name FROM application WHERE username_fk="{userid}"'
        )
        cursor.execute(query)
        results = [(name, appid) for name, appid in cursor]
        cursor.close()
        return results
