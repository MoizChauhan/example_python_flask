import os
import mysql.connector

def create_connection():
    db_host = "db_host"
    db_name = "name"
    db_user = "user"
    db_password = "pass"

    conn = mysql.connector.connect(
        host=db_host,
        database=db_name,
        user=db_user,
        password=db_password,
    )
    return conn

def create_tables():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255),
            username VARCHAR(255),
            phone VARCHAR(20),
            email VARCHAR(255),
            password VARCHAR(255),
            usertype VARCHAR(20),
            dateofbirth DATE
        )
    ''')
    conn.commit()
    conn.close()

def insert_user(name, username, phone, email, password, usertype, dateofbirth):
    conn = create_connection()
    cursor = conn.cursor()
    insert_query = "INSERT INTO users (name, username, phone, email, password, usertype, dateofbirth) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    data = (name, username, phone, email, password, usertype, dateofbirth)
    cursor.execute(insert_query, data)
    conn.commit()
    conn.close()

def search_user(username):
    conn = create_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM users WHERE username = %s"
    cursor.execute(query, (username,))
    
    user = cursor.fetchone()  # Fetch the first matching user (if any)

    conn.close()
    return user
