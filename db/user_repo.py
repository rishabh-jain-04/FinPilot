from db.db import db_connection

def create_user(username, email, password_hash):
    with db_connection() as connection:
        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)""",
            (username, email, password_hash),
        )
        connection.commit()

def get_user_by_email(email):
    with db_connection() as connection:
        cursor = connection.cursor()

        cursor.execute("""SELECT * FROM users WHERE email = ?""", (email,))
        return cursor.fetchone()