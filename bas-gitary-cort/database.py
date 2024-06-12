import sqlite3
from datetime import datetime

database = 'database.db'

def create_tables():
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS otbor (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            num_items INTEGER NOT NULL
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            otbor_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            price TEXT NOT NULL,
            FOREIGN KEY (otbor_id) REFERENCES otbor(id)
        )
    ''')
    
    conn.commit()
    conn.close()

def add_otbor(date, num_items):
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO otbor (date, num_items) VALUES (?, ?)
    ''', (date, num_items))
    
    last_id = cursor.lastrowid
    
    conn.commit()
    conn.close()
    return last_id

def add_product(otbor_id, name, price):
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO products (otbor_id, name, price) VALUES (?, ?, ?)
    ''', (otbor_id, name, price))
    
    conn.commit()
    conn.close()

def add_products(products):

    otbor_id = add_otbor(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), len(products)) 

    for product in products:
        add_product(otbor_id, *product)

def get_all_otbor():
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM otbor')
    rows = cursor.fetchall()
    
    conn.close()
    return rows

def get_all_products():
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM products')
    rows = cursor.fetchall()
    
    conn.close()
    return rows

def get_products_by_otbor(otbor_id):
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM products WHERE otbor_id = ?', (otbor_id,))
    rows = cursor.fetchall()
    
    conn.close()
    return rows