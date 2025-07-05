import sqlite3

def register(username, password):
    if not username.strip() or not password.strip():
        return "empty"

    try:
        conn = sqlite3.connect('inventory.db')
        c = conn.cursor()
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        conn.close()
        return "success"
    except sqlite3.IntegrityError:
        return "exists"
    except:
        return "error"

def login(username, password):
    conn = sqlite3.connect('inventory.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    result = c.fetchone()
    conn.close()
    return result is not None
