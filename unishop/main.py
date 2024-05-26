import aiohttp
import asyncio

import requests
from bs4 import BeautifulSoup

from tkinter import *
from tkinter import ttk

from datetime import datetime
from database import get_data_tables, get_products_by_number, get_last_date, insert_into_data_table, insert_into_products_table

# URLS

url = 'https://unishop.by/categories/diski/'
pages = [ f'{url}?page={i}' for  i in range(0, 5) ]

# Work with window

def show_dates_table():
    dates = get_data_tables()

    for item in table_dates.get_children():
        table_dates.delete(item)

    for date in dates:
        value = (date[0], date[1], date[2])
        table_dates.insert('', END, values=value)

def show_products_table(number):
    products = get_products_by_number(number)

    for item in table_products.get_children():
        table_products.delete(item)

    for product in products:
        if product[4]:
            value = (product[1], product[2], product[3], product[4])
        else:
            value = (product[1], product[2], product[3], 'Нету')
        table_products.insert('', END, values=value)

data_to_init = ()

def on_click(event):
    global data_to_init

    selected_item = table_dates.focus()
    data_to_init = table_dates.item(selected_item, 'values')

def init():
    show_products_table(int(data_to_init[0]))

# Parsers

def sync_parsing():
    all_items = []

    for i, page in enumerate(pages):
        response = requests.get(url=page)
        soup = BeautifulSoup(response.text, 'lxml')
        
        # Здесь прога получает товары 
        product_list = soup.find('div', {'class': 'product-list'})
        product_list_items = product_list.find_all('div', {'class': 'item'})

        # Здесь прога обрабатывает товары
        for i, item in enumerate(product_list_items):

            # Тут ты полуаешь название товара
            product_name = item.find('h3', {'class': 'name'}).find('a').text
        
            # Тут ты полуаешь цены товара
            price_items = item.find('div', {'class': 'price'})

            # Здесь ты обрабатываешь цены, делая из них массив
            price_list = price_items.text.strip().split(' ')
            
            # Если длина массива равна 5 (то есть у товара есть минимальная и максимальная цена), то делается две переменные, в одной указана минимальная, в другой указана максимальаня цена 
            if len(price_list) == 5:
                price_min = price_list[0]
                price_max = price_list[3]
            else:
                # Если длина массива не равняется 5, то цене с минимальной ценой присваивается то число что прога найдет, максимальной присвается занчение None
                price_min = price_list[0]
                price_max = None
            
            test_file += f'{i}. {product_name}; ({price_min}, {price_max})\n'

            all_items.append((product_name, price_min, price_max))
        
    cur_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    insert_into_data_table(cur_date, len(all_items))
    
    last_date = get_last_date()
    last_date_id = last_date[0]
    
    for item in all_items:
        insert_into_products_table(last_date_id, *item)

    show_dates_table()

async def async_parsing():
    all_items = []

    # Эта фунцкия работает точно также, просто она иначе выглядит

    for page in pages:
        async with aiohttp.ClientSession() as session:
            async with session.get(url=page, ssl=False) as response:
                soup = BeautifulSoup(await response.text(), 'lxml')

                product_list = soup.find('div', {'class': 'product-list'})
                product_list_items = product_list.find_all('div', {'class': 'item'})

                for item in product_list_items:
                    product_name = item.find('h3', {'class': 'name'}).find('a').text
                
                    price_items = item.find('div', {'class': 'price'})

                    price_list = price_items.text.strip().split(' ')
                    
                    if len(price_list) == 5:
                        price_min = price_list[0]
                        price_max = price_list[3]
                    else:
                        price_min = price_list[0]
                        price_max = None
                    
                    all_items.append((product_name, price_min, price_max))

    cur_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    insert_into_data_table(cur_date, len(all_items))
    
    last_date = get_last_date()
    last_date_id = last_date[0]
    
    for item in all_items:
        insert_into_products_table(last_date_id, *item)

    show_dates_table()

def start_async_parsing():
    asyncio.run(async_parsing())

# Window

root = Tk()
root.title(f'Парсер для {url}')
root.geometry("1000x500")
root.minsize(300,300)

root.columnconfigure(0, weight=1)
root.columnconfigure(2, weight=1)
root.rowconfigure(3, weight=1)

label = Label(text='Выбери тип парсинга: ')
label.grid(row=0, column=0, columnspan=3)

button = Button(text="Синхронный парсинг", command=sync_parsing)
button.grid(row=1, column=0, columnspan=3, sticky='ew', pady=2)

button = Button(text="Асинхронный парсинг", command=start_async_parsing)
button.grid(row=2, column=0, columnspan=3, sticky='ew', pady=2)

columns_dates = ('parsing_number', 'date', 'products_sum')

table_dates = ttk.Treeview(columns=columns_dates, show="headings")
table_dates.grid(row=3, column=0, sticky='nsew')

table_dates.heading("parsing_number", text="ID")
table_dates.heading("date", text="Дата")
table_dates.heading("products_sum", text="Товары")

table_dates.column("#1", stretch=NO, width=50)
table_dates.column("#2", stretch=YES, width=100)
table_dates.column("#3", stretch=YES, width=50)

show_dates_table()

table_dates.bind('<ButtonRelease-1>', on_click)

button = Button(text=">", command=init)
button.grid(row=3, column=1)

columns_products = ('parsing_number', 'title', 'price_min', 'price_max')
 
table_products = ttk.Treeview(columns=columns_products, show="headings")
table_products.grid(row=3, column=2, sticky='nsew')

table_products.heading("parsing_number", text="ID отбора")
table_products.heading("title", text="Название товара")
table_products.heading("price_min", text="Цена мин.")
table_products.heading("price_max", text="Цена макс.")

table_products.column("#1", stretch=NO, width=75)
table_products.column("#2", stretch=YES, width=100)
table_products.column("#3", stretch=NO, width=100)
table_products.column("#4", stretch=NO, width=100)

root.mainloop()