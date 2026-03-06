import os
import sqlite3

DATABASE_URL = os.environ.get("DATABASE_URL")

if DATABASE_URL:
    import psycopg2
    def get_conn():
        return psycopg2.connect(DATABASE_URL)
    PH = "%s"  # psycopg2 placeholder
else:
    def get_conn():
        return sqlite3.connect("safeway.db")
    PH = "?"   # sqlite3 placeholder


def create_tables():
    conn = get_conn()
    c = conn.cursor()

    c.execute(f'''
        CREATE TABLE IF NOT EXISTS deals (
            id {'SERIAL' if DATABASE_URL else 'INTEGER'} PRIMARY KEY,
            item TEXT NOT NULL,
            price TEXT NOT NULL
        )
    ''')

    c.execute(f'''
        CREATE TABLE IF NOT EXISTS purchases (
            id {'SERIAL' if DATABASE_URL else 'INTEGER'} PRIMARY KEY,
            item TEXT NOT NULL,
            count INTEGER DEFAULT 1
        )
    ''')

    conn.commit()
    conn.close()

def add_deals(deals):
    conn = get_conn()
    c = conn.cursor()
    c.execute("DELETE FROM deals")
    for deal in deals:
        c.execute(f"INSERT INTO deals (item, price) VALUES ({PH}, {PH})", (deal["item"], deal["price"]))
    conn.commit()
    conn.close()

def add_purchases(items):
    conn = get_conn()
    c = conn.cursor()
    for item in items:
        c.execute(f"SELECT count FROM purchases WHERE item = {PH}", (item,))
        row = c.fetchone()
        if row:
            c.execute(f"UPDATE purchases SET count = count + 1 WHERE item = {PH}", (item,))
        else:
            c.execute(f"INSERT INTO purchases (item, count) VALUES ({PH}, 1)", (item,))
    conn.commit()
    conn.close()

def get_all_deals():
    conn = get_conn()
    c = conn.cursor()
    c.execute("SELECT item, price FROM deals")
    rows = c.fetchall()
    conn.close()
    return [{"item": row[0], "price": row[1]} for row in rows]

def get_recommendations():
    conn = get_conn()
    c = conn.cursor()
    c.execute('''
        SELECT d.item, d.price FROM deals d
        JOIN purchases p ON d.item = p.item
    ''')
    rows = c.fetchall()
    conn.close()
    return [{"item": row[0], "price": row[1]} for row in rows]
