import sqlite3

database_name = 'database.db'

# Добавить данные в БД
def insert_parsing(date, items_num):
    conn = sqlite3.connect(database_name)
    cursor = conn.cursor()
    
    cursor.execute('''
    INSERT INTO Parsing (Date, Items_Num)
    VALUES (?, ?)
    ''', (date, items_num))
    
    conn.commit()
    conn.close()

    return cursor.lastrowid

def insert_results(parsing_id, results):
    conn = sqlite3.connect(database_name)
    cursor = conn.cursor()

    for result in results:

        name, article, brand, price, url = result

        cursor.execute('''
        INSERT INTO Results (Parsing_id, Name, Article, Brand, Price, Url)
        VALUES (?, ?, ?, ?, ?, ?)
        ''', (parsing_id, name, article, brand, price, url))
    
    conn.commit()
    conn.close()

# Получить все даты и продукты
def fetch_all_parsings():
    conn = sqlite3.connect(database_name)
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM Parsing')
    
    selections = cursor.fetchall()
    conn.close()

    return selections

def fetch_all_results():
    conn = sqlite3.connect(database_name)
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM Results')
    
    results = cursor.fetchall()
    conn.close()

    return results

# Получить данные по номеру отбора
def fetch_results_by_selection(parsing_id):
    conn = sqlite3.connect(database_name)
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM Results WHERE Parsing_id = ?', (parsing_id,))
    
    result = cursor.fetchall()
    conn.close()

    return result


conn = sqlite3.connect(database_name)
cur = conn.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS Parsing (
                    id INTEGER PRIMARY KEY,
                    Date DATE,
                    Items_Num INTEGER
                )''')

cur.execute('''CREATE TABLE IF NOT EXISTS Results (
                    id INTEGER PRIMARY KEY,
                    Parsing_id INTEGER,
                    Name TEXT,
                    Article INT,
                    Brand TEXT,
                    Price INT,
                    Url TEXT,
                    FOREIGN KEY (Parsing_id) REFERENCES Parsing(id)
                )''')

conn.commit()
conn.close()