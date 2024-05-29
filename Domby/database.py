import sqlite3
from datetime import datetime

database_name = 'divany.db'

def setup_database():
    with sqlite3.connect(database_name) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS CatalogSelections (
                CatalogID INTEGER PRIMARY KEY AUTOINCREMENT,
                DateCreated TEXT NOT NULL,
                TotalProducts INTEGER NOT NULL
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS CatalogProducts (
                CatalogID INTEGER,
                Name TEXT NOT NULL,
                Price INTEGER NOT NULL,
                FOREIGN KEY (CatalogID) REFERENCES CatalogSelections (CatalogID)
            )
        ''')
        conn.commit()

def insert_catalog(total_products):
    with sqlite3.connect(database_name) as conn:
        cursor = conn.cursor()
        creation_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute('INSERT INTO CatalogSelections (DateCreated, TotalProducts) VALUES (?, ?)', 
                       (creation_date, total_products))
        conn.commit()

def insert_product(catalog_id, name, price):
    with sqlite3.connect(database_name) as conn:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO CatalogProducts (CatalogID, Name, Price) VALUES (?, ?, ?)', 
                       (catalog_id, name, price))
        conn.commit()

def add_catalog_with_products(total_products, product_list):
    insert_catalog(total_products)
    with sqlite3.connect(database_name) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT MAX(CatalogID) FROM CatalogSelections')
        catalog_id = cursor.fetchone()[0]
        for product in product_list:
            insert_product(catalog_id, *product)

def fetch_all_products():
    with sqlite3.connect(database_name) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM CatalogProducts')
        return cursor.fetchall()

def fetch_products_by_catalog(catalog_id):
    with sqlite3.connect(database_name) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM CatalogProducts WHERE CatalogID = ?', (catalog_id,))
        return cursor.fetchall()

def fetch_all_catalogs():
    with sqlite3.connect(database_name) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM CatalogSelections')
        return cursor.fetchall()
