import mysql.connector
from mysql.connector import Error

def connect_db():
    """Connect to MySQL server without database"""
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='username',
            password='password'

        )
        if connection.is_connected():
            print("Connected to MySQL server.")
            return connection
    except Error as e:
        print("Error connecting to MySQL server:", e)
        return None

def create_database(connection):
    """Create databse ALX_prodev ifit doesn't exist"""
    try:
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev")
        print("Database 'ALX_prodev' is ready.")
    except Error as e:
        print("Failed to create database:", e)

def create_table(connection):
    """Create user_data table if it doesn't exist"""
    try:
        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_data (
                user_id CHAR(36) PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL,
                age DECIMAL(5, 2) NOT NULL,
                INDEX(email)
            )
        """)
        print("Table 'user_data' is ready.")
    except Error as e:
        print("Failed to create table:", e)



