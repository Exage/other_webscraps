import sqlite3
 
con = sqlite3.connect("metanit.db")
cursor = con.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS Contractor_Table (
                    ContractorID INTEGER PRIMARY KEY,
                    Name TEXT,
                    GroupID INTEGER,
                    RegionID INTEGER,
                    UNN TEXT,
                    Adr TEXT,
                    FOREIGN KEY (GroupID) REFERENCES Group_Table(GroupID),
                    FOREIGN KEY (RegionID) REFERENCES Region_Table(RegionID)
                )''')

cursor.execute('''CREATE TABLE IF NOT EXISTS Affiliate_Table (
                    AffiliateID INTEGER PRIMARY KEY,
                    ContractorID INTEGER,
                    Name TEXT,
                    Adr TEXT,
                    FOREIGN KEY (ContractorID) REFERENCES Contractor_Table(ContractorID)
                )''')

cursor.execute('''CREATE TABLE IF NOT EXISTS Account_Table (
                    AccountID INTEGER PRIMARY KEY,
                    ContractorID INTEGER,
                    Bank TEXT,
                    Account TEXT,
                    Currency TEXT,
                    FOREIGN KEY (ContractorID) REFERENCES Contractor_Table(ContractorID)
                )''')

cursor.execute('''CREATE TABLE IF NOT EXISTS Group_Table (
                    GroupID INTEGER PRIMARY KEY,
                    Name TEXT
                )''')

cursor.execute('''CREATE TABLE IF NOT EXISTS Region_Table (
                    RegionID INTEGER PRIMARY KEY,
                    Name TEXT
                )''')

cursor.executemany("INSERT INTO Group_Table (GroupID, Name) VALUES (?, ?)",
                   [(1, 'IT компании'), (2, 'Транспортные компании')])

cursor.executemany("INSERT INTO Region_Table (RegionID, Name) VALUES (?, ?)",
                   [(1, 'Брестская область'), (2, 'Миснкая область'), (3, 'Гродненская область')])

cursor.executemany("INSERT INTO Contractor_Table (ContractorID, Name, GroupID, RegionID, UNN, Adr) VALUES (?, ?, ?, ?, ?, ?)",
                   [(1, 'ISoft', 1, 1, 'ID8257214', 'г. Брест, просп. Машерова 6а'),
                    (2, 'Yandex', 2, 2, 'ID5192354', 'г. Минск, проспект Дзержинского 5'),
                    (3, 'Intex Soft', 1, 3, 'ID9537154', 'г. Гродно, ул. Богуцкого 5/4')])

cursor.executemany("INSERT INTO Affiliate_Table (AffiliateID, ContractorID, Name, Adr) VALUES (?, ?, ?, ?)",
                   [(1, 1, 'Интерстеллар', 'г.Брест, ул. Гоздецкого, 8'),
                    (2, 2, 'ТРАСКО ЛОГИСТИКА ООО', 'г.Минск, пр. Дзержинского 104'),
                    (3, 3, 'АВСУС', 'г.Гродно, ул. Подольная 37')])

cursor.executemany("INSERT INTO Account_Table (AccountID, ContractorID, Bank, Account, Currency) VALUES (?, ?, ?, ?, ?)",
                   [(1, 1, 'БеларусьБанк 1', 'SSD7455187645', 'BYN'),
                    (2, 2, 'Альфа-Банк', 'HDD3682509185', 'BYN'),
                    (3, 3, 'БелГазпромБанк', 'CSS4569823126', 'USD')])

cursor.execute("SELECT * FROM Contractor_Table;")
Contractors_Data = cursor.fetchall()

cursor.execute("SELECT * FROM Affiliate_Table;")
Affirates_Data = cursor.fetchall()

cursor.execute("SELECT * FROM Account_Table;")
Accounts_Data = cursor.fetchall()

with open("data.txt", 'w') as file:
        for Str in Contractors_Data:
            file.write(", ".join(map(str, Str)) + '\n')
            file.write('\n')
        file.write('\n')
        for Str in Affirates_Data:
            file.write(", ".join(map(str, Str)) + '\n')
            file.write('\n')
        file.write('\n')
        for Str in Accounts_Data:
            file.write(", ".join(map(str, Str)) + '\n')
            file.write('\n')

# cursor.execute("DROP TABLE IF EXISTS Contractor_Table;")
# cursor.execute("DROP TABLE IF EXISTS Affiliate_Table;")
# cursor.execute("DROP TABLE IF EXISTS Account_Table;")
# cursor.execute("DROP TABLE IF EXISTS Group_Table;")
# cursor.execute("DROP TABLE IF EXISTS Region_Table;")

con.commit()
con.close()