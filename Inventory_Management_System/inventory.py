import sqlite3

def add_product(name, quantity, price):
    conn = sqlite3.connect('inventory.db')
    c = conn.cursor()
    c.execute("INSERT INTO inventory (name, quantity, price) VALUES (?, ?, ?)", (name, quantity, price))
    conn.commit()

def update_product(id, name, quantity, price):
    conn = sqlite3.connect('inventory.db')
    c = conn.cursor()
    c.execute("UPDATE inventory SET name=?, quantity=?, price=? WHERE id=?", (name, quantity, price, id))
    conn.commit()

def delete_product(id):
    conn = sqlite3.connect('inventory.db')
    c = conn.cursor()
    c.execute("DELETE FROM inventory WHERE id=?", (id,))
    conn.commit()

def get_all_products():
    conn = sqlite3.connect('inventory.db')
    c = conn.cursor()
    c.execute("SELECT * FROM inventory")
    return c.fetchall()

def get_low_stock(threshold=10):
    conn = sqlite3.connect('inventory.db')
    c = conn.cursor()
    c.execute("SELECT * FROM inventory WHERE quantity < ?", (threshold,))
    return c.fetchall()
