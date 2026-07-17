from db.db import get_connection


def save_message(user_id, role, message, intent=None):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO conversations (user_id, role, message, intent)
        VALUES (?, ?, ?, ?)
    """, (user_id, role, message, intent))

    connection.commit()
    connection.close()


def get_conversation_history(user_id, limit=20):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT role, message, intent, created_at
        FROM conversations
        WHERE user_id = ?
        ORDER BY created_at DESC
        LIMIT ?
    """, (user_id, limit))

    rows = cursor.fetchall()
    connection.close()

    return [dict(row) for row in rows]
