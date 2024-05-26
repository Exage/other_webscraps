import sqlite3

# Добавить данные в БД
def insert_selection(selection_date, items_count):
    conn = sqlite3.connect('phone_data.db')
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO selection (selection_date, items_count)
    VALUES (?, ?)
    ''', (selection_date, items_count))
    conn.commit()
    conn.close()
    return cursor.lastrowid

def insert_product(selection_id, product_name, product_price):
    conn = sqlite3.connect('phone_data.db')
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO product (selection_id, product_name, product_price)
    VALUES (?, ?, ?)
    ''', (selection_id, product_name, product_price))
    conn.commit()
    conn.close()

# Получить все даты и продукты
def fetch_all_selections():
    conn = sqlite3.connect('phone_data.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM selection')
    selections = cursor.fetchall()
    conn.close()
    return selections

def fetch_all_products():
    conn = sqlite3.connect('phone_data.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM product')
    products = cursor.fetchall()
    conn.close()
    return products

# Получить данные по номеру отбора
def fetch_products_by_selection(selection_id):
    conn = sqlite3.connect('phone_data.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM product WHERE selection_id = ?', (selection_id,))
    products = cursor.fetchall()
    conn.close()
    return products