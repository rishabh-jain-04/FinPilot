from db.db import db_connection


def save_message(user_id, role, message, intent=None):
    with db_connection() as connection:
        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO conversations (user_id, role, message, intent)
            VALUES (?, ?, ?, ?)
        """, (user_id, role, message, intent))

        connection.commit()


def get_conversation_history(user_id, limit=20):
    with db_connection() as connection:
        cursor = connection.cursor()

        cursor.execute("""
            SELECT role, message, intent, created_at
            FROM conversations
            WHERE user_id = ?
            ORDER BY created_at DESC
            LIMIT ?
        """, (user_id, limit))

        rows = cursor.fetchall()
        return [dict(row) for row in rows]
