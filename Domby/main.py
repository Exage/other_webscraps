import tkinter as tk
from tkinter import ttk

import asyncio
import aiohttp
import requests
from bs4 import BeautifulSoup

from database import setup_database, add_catalog_with_products, fetch_all_catalogs, fetch_all_products, fetch_products_by_catalog

links = [ f'https://www.dom.by/gds/divany/brest/?page={i}' for i in range(1, 6) ]

setup_database()

def parse_page(soup):

    items = soup.select('div.gdsItem__cart')
    items_handled = list()

    for item in items:
        name = item.find('div', 'gdsItem__title').text
        price = item.find('span', 'PriceStr__value').text + ' BYN'

        if 'Цену уточняйте у продавца' in price:
            price = 'Не указана'

        items_handled.append([name, price])

    return items_handled

def parse_page_sync():

    product_list = list()

    for link in links:
        page = requests.get(link)
        soup = BeautifulSoup(page.text, 'html.parser')

        product_list.extend(parse_page(soup))

    total_products = len(product_list)
    add_catalog_with_products(total_products, product_list)

async def parse_page_async():

    product_list = list()

    for link in links:
        async with aiohttp.ClientSession() as session:
            async with session.get(url=link, ssl=False) as response:
                soup = BeautifulSoup(await response.text(), 'html.parser')

                product_list.extend(parse_page(soup))

    total_products = len(product_list)
    add_catalog_with_products(total_products, product_list)

def button1_action():
    # Placeholder for button 1 action
    pass

def button2_action():
    # Placeholder for button 2 action
    pass

def update_catalogs_table():
    for i in catalogs_table.get_children():
        catalogs_table.delete(i)
    for catalog in fetch_all_catalogs():
        catalogs_table.insert('', 'end', values=catalog)

def update_products_table(catalog_id):
    for i in products_table.get_children():
        products_table.delete(i)
    for product in fetch_products_by_catalog(catalog_id):
        products_table.insert('', 'end', values=product)

def on_catalog_select(event):
    selected_item = catalogs_table.selection()[0]
    catalog_id = catalogs_table.item(selected_item, 'values')[0]
    result_label.config(text=f'Результат отбора [{catalog_id}]')
    update_products_table(catalog_id)

setup_database()

# Tkinter GUI
root = tk.Tk()
root.title('Catalog Manager')

root.rowconfigure(2, weight=1)

# Buttons
button1 = tk.Button(root, text='Button 1', command=button1_action)
button1.grid(row=0, column=0, padx=5, pady=5)

button2 = tk.Button(root, text='Button 2', command=button2_action)
button2.grid(row=0, column=1, padx=5, pady=5)

# Label
result_label = tk.Label(root, text='Выберите дату отбора')
result_label.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

# Catalogs Table
catalogs_table = ttk.Treeview(root, columns=('CatalogID', 'DateCreated', 'TotalProducts'), show='headings')
catalogs_table.heading('CatalogID', text='CatalogID')
catalogs_table.heading('DateCreated', text='DateCreated')
catalogs_table.heading('TotalProducts', text='TotalProducts')
catalogs_table.grid(row=2, column=0, padx=5, pady=5, sticky='NSEW')

# Products Table
products_table = ttk.Treeview(root, columns=('CatalogID', 'Name', 'Price'), show='headings')
products_table.heading('CatalogID', text='CatalogID')
products_table.heading('Name', text='Name')
products_table.heading('Price', text='Price')
products_table.grid(row=2, column=1, padx=5, pady=5, sticky='NSEW')

# Bind selection event
catalogs_table.bind('<<TreeviewSelect>>', on_catalog_select)

update_catalogs_table()

root.mainloop()