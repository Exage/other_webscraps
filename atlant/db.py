import sqlite3

db_name = 'atlant.db'

def insert_selection(selection_date, items_count):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO selection (selection_date, items_count)
    VALUES (?, ?)
    ''', (selection_date, items_count))
    conn.commit()
    conn.close()
    return cursor.lastrowid

def insert_product(selection_id, product_name, product_price):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO product (selection_id, product_name, product_price)
    VALUES (?, ?, ?)
    ''', (selection_id, product_name, product_price))
    conn.commit()
    conn.close()

def fetch_all_selections():
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM selection')
    selections = cursor.fetchall()
    conn.close()
    return selections

def fetch_all_products():
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM product')
    products = cursor.fetchall()
    conn.close()
    return products

def fetch_products_by_selection(selection_id):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM product WHERE selection_id = ?', (selection_id,))
    products = cursor.fetchall()
    conn.close()
    return products

def init_db():
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS selection (
        selection_id INTEGER PRIMARY KEY,
        selection_date DATE,
        items_count INTEGER
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS product (
        selection_id INTEGER,
        product_name TEXT,
        product_price REAL,
        FOREIGN KEY(selection_id) REFERENCES selection(selection_id)
    )
    ''')

    conn.commit()
    conn.close()