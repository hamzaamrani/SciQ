from config import DB_CONFIG
import mysql.connector
import json

# TODO: BLUEPRINT FLASK
# TODO: mysql alchemy

def start_connection():
    print("Connecting to DB")
    connection = mysql.connector.connect(**DB_CONFIG)
    return connection

def check_exist(self, username):
    connection = start_connection()
    cursor = connection.cursor()
    query = f'SELECT UNIQUE * FROM User WHERE username="{username}"'
    cursor.execute(query)
    results = [user for user in cursor]
    cursor.close()
    connection.close()
    return results[0] > 0
    
def check_credentials(self, username, password):
    connection = start_connection()
    cursor = connection.cursor()
    query = f'SELECT UNIQUE * FROM User WHERE username="{username}" and password="{password}"'
    cursor.execute(query)
    results = [user for user in cursor]
    cursor.close()
    return results[0]

def signup(self, username, password):
    connection = start_connection()
    connection.open()
    if self.check_exist(username):
        raise Exception("Username already taken!")

    query = f'INSERT INTO User (username, password) VALUES ("{username}", "{password}"'
    cursor = connection.cursor()
    cursor.execute(query)
    cursor.close()
    connection.close()
    
    return True


