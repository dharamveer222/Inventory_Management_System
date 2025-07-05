import sqlite3

def init_db():
    conn = sqlite3.connect('inventory.db')
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        username TEXT UNIQUE,
        password TEXT
    )""")
    c.execute("""CREATE TABLE IF NOT EXISTS inventory (
        id INTEGER PRIMARY KEY,
        name TEXT,
        quantity INTEGER,
        price REAL
    )""")
    conn.commit()
    conn.close()
