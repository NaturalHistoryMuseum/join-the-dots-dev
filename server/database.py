from flask import current_app as app
import mysql.connector

# Create a connection
def get_db_connection():
    return mysql.connector.connect(
        host=app.config['MYSQL_HOST'],
        user=app.config['MYSQL_USER'],
        password=app.config['MYSQL_PASSWORD'],
        database=app.config['MYSQL_DB']
    )

# Create a connection to the secondary database
def get_test_db_connection():
    return mysql.connector.connect(
        host=app.config['SECONDARY_DB_HOST'],
        user=app.config['SECONDARY_DB_USER'],
        password=app.config['SECONDARY_DB_PASSWORD'],
        database=app.config['SECONDARY_DB_NAME']
    )