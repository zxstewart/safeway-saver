import sqlite3

DB_FILE = "safeway.db"

def create_tables():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()

    # Deals table
    c.execute('''
        CREATE TABLE IF NOT EXISTS deals (
            id INTEGER PRIMARY KEY,
            item TEXT NOT NULL,
            price TEXT NOT NULL
        )
    ''')

    # Purchase history table
    c.execute('''
        CREATE TABLE IF NOT EXISTS purchases (
            id INTEGER PRIMARY KEY,
            item TEXT NOT NULL,
            count INTEGER DEFAULT 1
        )
    ''')

    conn.commit()
    conn.close()

def add_deals(deals):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("DELETE FROM deals")  # Clear old data
    for deal in deals:
        c.execute("INSERT INTO deals (item, price) VALUES (?, ?)", (deal["item"], deal["price"]))
    conn.commit()
    conn.close()

def add_purchases(items):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    for item in items:
        c.execute("SELECT count FROM purchases WHERE item = ?", (item,))
        row = c.fetchone()
        if row:
            c.execute("UPDATE purchases SET count = count + 1 WHERE item = ?", (item,))
        else:
            c.execute("INSERT INTO purchases (item, count) VALUES (?, 1)", (item,))
    conn.commit()
    conn.close()

def get_all_deals():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT item, price FROM deals")
    rows = c.fetchall()
    conn.close()
    return [{"item": row[0], "price": row[1]} for row in rows]

def get_recommendations():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''
        SELECT d.item, d.price FROM deals d
        JOIN purchases p ON d.item = p.item
    ''')
    rows = c.fetchall()
    conn.close()
    return [{"item": row[0], "price": row[1]} for row in rows]
