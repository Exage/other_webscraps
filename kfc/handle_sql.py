import sqlite3
from datetime import datetime

database_name = 'kfcdb.db'

def make_db():
    conn = sqlite3.connect(database_name)
    cur = conn.cursor()

    cur.execute('''CREATE TABLE IF NOT EXISTS Selection (
                    Selection_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    Selection_date TEXT NOT NULL,
                    Products_number INTEGER NOT NULL
                )''')

    cur.execute('''CREATE TABLE IF NOT EXISTS Products (
                    Selection_id INTEGER,
                    Product_name TEXT,
                    Product_price REAL,
                    FOREIGN KEY (Selection_id) REFERENCES Selection (Selection_id)
                )''')

    conn.commit()
    conn.close()

def add_selection(Products_number):
    conn = sqlite3.connect(database_name)
    cursor = conn.cursor()
    
    Selection_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute('INSERT INTO Selection (Selection_date, Products_number) VALUES (?, ?)', (Selection_date, Products_number))
    
    conn.commit()
    conn.close()

def add_product(Selection_id, Product_name, Product_price):
    conn = sqlite3.connect(database_name)
    cursor = conn.cursor()
    
    cursor.execute('INSERT INTO Products (Selection_id, Product_name, Product_price) VALUES (?, ?, ?)', 
                   (Selection_id, Product_name, Product_price))
    
    conn.commit()
    conn.close()

def add_products(Products_number, Product_list):
    conn = sqlite3.connect(database_name)
    cursor = conn.cursor()

    add_selection(Products_number)
    
    cursor.execute('SELECT MAX(Selection_id) FROM Selection')
    Selection_id = cursor.fetchone()[0]
    
    for product in Product_list:
        Product_name, Product_price = product
        add_product(Selection_id, Product_name, Product_price)
    
    conn.close()

def get_products_table():
    conn = sqlite3.connect(database_name)
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM Products')
    products = cursor.fetchall()

    return products

def get_products_item(number):
    conn = sqlite3.connect(database_name)
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM Products WHERE Selection_id = ?', (number,))
    product = cursor.fetchall()

    return product

def get_selections_table():
    conn = sqlite3.connect(database_name)
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM Selection')
    selection = cursor.fetchall()

    return selection