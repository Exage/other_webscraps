import sqlite3

database_name = 'unidb.db'

def get_data_tables():
    conn = sqlite3.connect(database_name)
    cur = conn.cursor()

    cur.execute("SELECT * FROM Parse_Date_Table;")
    Parse_Date_Table = cur.fetchall()

    conn.commit()
    conn.close()

    return Parse_Date_Table

def get_products_by_number(product_number):
    conn = sqlite3.connect(database_name)
    cur = conn.cursor()

    cur.execute("SELECT * FROM Products_Table WHERE Parse_Date_ID = ?", (product_number,))
    product = cur.fetchall()

    conn.commit()
    conn.close()

    return product

def get_last_date():
    dates = get_data_tables()

    return dates[len(dates) - 1]

def insert_into_data_table(date, products_num):
    conn = sqlite3.connect(database_name)
    cur = conn.cursor()

    cur.execute("INSERT INTO Parse_Date_Table (Date, Products_Num) VALUES (?, ?)",
                   (date, products_num))
    
    conn.commit()
    conn.close()

def insert_into_products_table(parse_date_id, name, price_min, price_max):
    conn = sqlite3.connect(database_name)
    cur = conn.cursor()

    cur.execute("INSERT INTO Products_Table (Parse_Date_Id, Name, Price_min, Price_max) VALUES (?, ?, ?, ?)",
                   (parse_date_id, name, price_min, price_max))
    
    conn.commit()
    conn.close()

conn = sqlite3.connect(database_name)
cur = conn.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS Parse_Date_Table (
                    id INTEGER PRIMARY KEY,
                    Date DATE,
                    Products_Num INTEGER
                )''')

cur.execute('''CREATE TABLE IF NOT EXISTS Products_Table (
                    id INTEGER PRIMARY KEY,
                    Parse_Date_ID INTEGER,
                    Name TEXT,
                    Price_min REAL,
                    Price_max REAL,
                    FOREIGN KEY (Parse_Date_ID) REFERENCES Parse_Date_Table(id)
                )''')

conn.commit()
conn.close()