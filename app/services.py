from config import connection_string, DB_CONFIG
import json
import mysql.connector
                        
# TODO: BLUEPRINT FLASK
# TODO: mysql alchemy

class UserService:
    def __init__(self):
        print("Connecting")
        self.connection = mysql.connector.connect(**DB_CONFIG)
        
    def check_exist(self, username):
        cursor = self.connection.cursor()
        query = f'SELECT * FROM User WHERE username="{username}"'
        cursor.execute(query)
        results = [user for user in cursor]
        cursor.close()
        return len(results) > 0
    
    def check_credentials(self, username, password):
        cursor = self.connection.cursor()
        query = f"select * from User where username='{username}' and password='{password}'"
        cursor.execute(query)
        results = [user for user in cursor]
        cursor.close()
        return len(results) > 0

    def signup(self, username, password):
        cursor = self.connection.cursor()
        if self.check_exist(username):
            raise Exception("Username already taken!")

        query = f'INSERT INTO User (username, password) VALUES ("{username}", "{password}")'
        cursor = self.connection.cursor()
        cursor.execute(query)
        self.connection.commit()
        cursor.close()        
        return True


