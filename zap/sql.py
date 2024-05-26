import sqlite3
from datetime import datetime

database_name = 'zap.db'

def add_selection(number_of_products):
    conn = sqlite3.connect(database_name)
    cursor = conn.cursor()
    
    selection_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute('INSERT INTO Selection (SelectionDate, NumberOfProducts) VALUES (?, ?)', (selection_date, number_of_products))
    
    conn.commit()
    conn.close()

def add_product(selection_id, product_name, product_article, product_price, product_brand):
    conn = sqlite3.connect(database_name)
    cursor = conn.cursor()
    
    cursor.execute('INSERT INTO Products (SelectionID, ProductName, ProductArticle, ProductPrice, ProductBrand) VALUES (?, ?, ?, ?, ?)', 
                   (selection_id, product_name, product_article, product_price, product_brand))
    
    conn.commit()
    conn.close()

def insert_data(product_list):
    add_selection(len(product_list))
    
    conn = sqlite3.connect(database_name)
    cursor = conn.cursor()
    
    cursor.execute('SELECT MAX(SelectionID) FROM Selection')
    selection_id = cursor.fetchone()[0]
    
    for product in product_list:
        product_name, product_article, product_price, product_brand = product
        add_product(selection_id, product_name, product_article, product_price, product_brand)
    
    conn.close()

def get_products():
    conn = sqlite3.connect(database_name)
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM Products')
    products = cursor.fetchall()

    return products

def get_products_by_num(num):
    conn = sqlite3.connect(database_name)
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM Products WHERE SelectionID = ?', (num,))
    selection = cursor.fetchall()

    return selection

def get_selections():
    conn = sqlite3.connect(database_name)
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM Selection')
    selections = cursor.fetchall()

    return selections

conn = sqlite3.connect(database_name)
cur = conn.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS Selection (
                SelectionID INTEGER PRIMARY KEY AUTOINCREMENT,
                SelectionDate Date NOT NULL,
                NumberOfProducts INTEGER NOT NULL
            )''')

cur.execute('''CREATE TABLE IF NOT EXISTS Products (
                SelectionID INTEGER,
                ProductName TEXT NOT NULL,
                ProductArticle TEXT NOT NULL,
                ProductPrice REAL NOT NULL,
                ProductBrand TEXT NOT NULL,
                FOREIGN KEY (SelectionID) REFERENCES Selection (SelectionID)
            )''')

conn.commit()
conn.close()