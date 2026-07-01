import sqlite3
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent

DATABASE_PATH = BASE_DIR / "finpilot.db"

SCHEMA_PATH = BASE_DIR / "schema.sql"

def get_connection():
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    return connection

def init_db():
    connection = get_connection()

    with open(SCHEMA_PATH, "r", encoding="utf-8") as schema_file:
        connection.executescript(schema_file.read())

    connection.commit()
    connection.close()