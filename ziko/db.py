import sqlite3
import datetime

database_name = 'ziko.db'

def get_dates_from_db():
    conn = sqlite3.connect(database_name)
    cur = conn.cursor()

    cur.execute("SELECT * FROM Parsing_Table;")
    Parsing_Table = cur.fetchall()

    conn.commit()
    conn.close()

    return Parsing_Table

def get_items_from_db(n):
    conn = sqlite3.connect(database_name)
    cur = conn.cursor()

    cur.execute("SELECT * FROM Parsing_Result_Table WHERE Parsing_Table_id = ?", (n,))
    product = cur.fetchall()

    conn.commit()
    conn.close()

    return product

def get_item_from_db(n):
    conn = sqlite3.connect(database_name)
    cur = conn.cursor()

    cur.execute("SELECT * FROM Parsing_Result_Table WHERE id = ?", (n,))
    product = cur.fetchall()

    conn.commit()
    conn.close()

    return product

def push_date_to_db(date, items_num, parsing_type):
    conn = sqlite3.connect(database_name)
    cur = conn.cursor()

    cur.execute("INSERT INTO Parsing_Table (Date, Items_Num, Parsing_Type) VALUES (?, ?, ?)",
                   (date, items_num, parsing_type))
    
    conn.commit()
    conn.close()

    return cur.lastrowid

def push_item_to_db(parsing_table_id, name, price, link, page):
    conn = sqlite3.connect(database_name)
    cur = conn.cursor()

    cur.execute("INSERT INTO Parsing_Result_Table (Parsing_Table_id, Name, Price, Link, Page) VALUES (?, ?, ?, ?, ?)",
                   (parsing_table_id, name, price, link, page))
    
    conn.commit()
    conn.close()

def push_to_db(items, parsing_type):
    date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    id = push_date_to_db(date, len(items), parsing_type)

    for item in items:
        push_item_to_db(id, *item.values())


conn = sqlite3.connect(database_name)
cur = conn.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS Parsing_Table (
                    id INTEGER PRIMARY KEY,
                    Date DATE,
                    Items_Num INTEGER,
                    Parsing_Type TEXT
                )''')

cur.execute('''CREATE TABLE IF NOT EXISTS Parsing_Result_Table (
                    id INTEGER PRIMARY KEY,
                    Parsing_Table_id INTEGER,
                    Name TEXT,
                    Price TEXT,
                    Link TEXT,
                    Page INTEGER,
                    FOREIGN KEY (Parsing_Table_id) REFERENCES Parsing_Table(id)
                )''')

conn.commit()
conn.close()