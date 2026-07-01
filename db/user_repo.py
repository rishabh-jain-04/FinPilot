from db.db import get_connection

def create_user(username, email, password_hash):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)""",
        (username, email, password_hash),
    )
    connection.commit()
    connection.close()

def get_user_by_email(email):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""SELECT * FROM users WHERE email = ?""", (email,))
    user = cursor.fetchone()

    connection.close()
    return user