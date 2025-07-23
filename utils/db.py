import sqlite3
import os

DB_PATH = "data/db.sqlite3"

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    if not os.path.exists(DB_PATH):
        conn = get_db_connection()
        conn.execute("""
            CREATE TABLE history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                item TEXT NOT NULL,
                count INTEGER DEFAULT 1
            )
        """)
        conn.commit()
        conn.close()

def update_history(items):
    conn = get_db_connection()
    for item in items:
        cursor = conn.execute("SELECT count FROM history WHERE item = ?", (item,))
        row = cursor.fetchone()
        if row:
            conn.execute("UPDATE history SET count = ? WHERE item = ?", (row["count"] + 1, item))
        else:
            conn.execute("INSERT INTO history (item, count) VALUES (?, 1)", (item,))
    conn.commit()
    conn.close()

def get_recommended_items(current_deals):
    conn = get_db_connection()
    cursor = conn.execute("SELECT item FROM history")
    past_items = set(row["item"] for row in cursor.fetchall())
    conn.close()
    return [deal for deal in current_deals if deal["item"] in past_items]
