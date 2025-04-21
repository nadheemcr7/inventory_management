import sqlite3

def get_connection():
    conn = sqlite3.connect("inventory.db")
    return conn

def create_tables():
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Products (
        product_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        category TEXT,
        price REAL,
        stock INTEGER
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Sales (
        sale_id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_id INTEGER,
        quantity_sold INTEGER,
        date TEXT,
        FOREIGN KEY (product_id) REFERENCES Products(product_id)
    )
    """)

    conn.commit()
    conn.close()