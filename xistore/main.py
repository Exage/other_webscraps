from tkinter import *
from tkinter import ttk

import requests
import aiohttp
import asyncio
from bs4 import BeautifulSoup
import sqlite3
from datetime import datetime

from parse_html import parse_html
from db import insert_selection, insert_product, fetch_all_selections, fetch_all_products, fetch_products_by_selection

urls = [
    'https://xistore.by/catalog/telefony/?PAGEN_1=1',
    'https://xistore.by/catalog/telefony/?PAGEN_1=2',
    'https://xistore.by/catalog/telefony/?PAGEN_1=3',
    'https://xistore.by/catalog/telefony/?PAGEN_1=4'
]

# Get and handle HTML data
def get_html_sync(urls):
    data = list()

    for url in urls:
        request = requests.get(url)
        soup = BeautifulSoup(request.text, 'html.parser')
        data.extend(parse_html(soup))

    selection_id = insert_selection(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), len(data))
    
    for item in data:
        insert_product(selection_id, *item)
    
    show_selections()
    show_all_products()

async def get_html_async(urls):
    data = list()

    for url in urls:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, ssl=False) as response:
                soup = BeautifulSoup(await response.text(), 'html.parser')
                data.extend(parse_html(soup))

    selection_id = insert_selection(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), len(data))

    for item in data:
        insert_product(selection_id, *item)
    
    show_selections()
    show_all_products()

# Make DB
conn = sqlite3.connect('phone_data.db')
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

# Interface

def show_all_products():
    products_list = fetch_all_products()

    for product in products.get_children():
        products.delete(product)

    for product in products_list:
        value = (product[0], product[1], product[2])
        products.insert('', END, values=value)

def show_first_products():
    products_list = fetch_products_by_selection(1)

    for product in products.get_children():
        products.delete(product)

    for product in products_list:
        value = (product[0], product[1], product[2])
        products.insert('', END, values=value)

def show_last_products():
    selections = fetch_all_selections()
    products_list = fetch_products_by_selection(len(selections))

    for product in products.get_children():
        products.delete(product)

    for product in products_list:
        value = (product[0], product[1], product[2])
        products.insert('', END, values=value)

def show_selections():
    selections_list = fetch_all_selections()

    for selection in selections.get_children():
        selections.delete(selection)

    for selection in selections_list:
        value = (selection[0], selection[1], selection[2])
        selections.insert('', END, values=value)

def btn_sync():
    get_html_sync(urls)

def btn_async():
    asyncio.run(get_html_async(urls))

root = Tk()
root.geometry('1200x800')

# root.columnconfigure(0, weight=0)
root.columnconfigure(1, weight=1)
root.rowconfigure(3, weight=1)

button_sync_data = Button(root, text='Получить данные синхронно', width=20, command=btn_sync)
button_sync_data.grid(row=0, column=0, columnspan=2, pady=5)

button_async_data = Button(root, text='Получить данные асинхронно', width=20, command=btn_async)
button_async_data.grid(row=1, column=0, columnspan=2, pady=5)

button_async_data = Button(root, text='Показать все товары', command=show_all_products)
button_async_data.grid(row=5, column=0, columnspan=2, pady=5)

button_async_data = Button(root, text='Показать последний отбор', command=show_last_products)
button_async_data.grid(row=6, column=0, columnspan=2, pady=5)

button_async_data = Button(root, text='Показать первый отбор', command=show_first_products)
button_async_data.grid(row=7, column=0, columnspan=2, pady=5)

selections_label = Label(root, text='Таблица Отбора')
selections_label.grid(row=2, column=0, pady=10)
selections = ttk.Treeview(root, columns=('selection_id', 'selection_date', 'items_count'), show='headings')
selections.heading('selection_id', text='ID отбора')
selections.heading('selection_date', text='Дата')
selections.heading('items_count', text='Количество продуктов')
selections.column("#1", stretch=NO, width=100)
selections.column("#2", stretch=NO)
selections.column("#3", stretch=NO, width=150)
selections.grid(row=3, column=0, padx=5, sticky='nsew')

show_selections()

products_label = Label(root, text='Таблица Товаров')
products_label.grid(row=2, column=1, pady=10)
products = ttk.Treeview(root, columns=('selection_id', 'product_name', 'product_price'), show='headings')
products.heading('selection_id', text='ID отбора')
products.heading('product_name', text='Название смартфона')
products.heading('product_price', text='Цена')
products.column("#1", stretch=NO, width=100)
products.column("#2", stretch=YES)
products.column("#3", stretch=NO, width=150)
products.grid(row=3, column=1, padx=5, sticky='nsew')

show_all_products()

if __name__ == '__main__':
    root.mainloop()