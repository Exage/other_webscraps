from tkinter import *
from tkinter import ttk

import asyncio

from get_data import parse_html_sync, parse_html_async
from database import get_all_otbor, get_products_by_otbor

def update_otbor_table():
    for i in otbor_table.get_children():
        otbor_table.delete(i)
    for catalog in get_all_otbor():
        otbor_table.insert('', 'end', values=catalog)

def update_products_table(catalog_id):
    for i in products_table.get_children():
        products_table.delete(i)
    for product in get_products_by_otbor(catalog_id):
        products_table.insert('', 'end', values=product)

def on_catalog_select(event):
    selected_item = otbor_table.selection()
    if selected_item:
        catalog_id = otbor_table.item(selected_item[0], 'values')[0]
        result_label.config(text=f'Выбран результат отбора №{catalog_id}')
        update_products_table(catalog_id)

# Tkinter GUI
root = Tk()
root.geometry('1200x800')
root.title('Парсер')

root.rowconfigure(2, weight=1)
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)

def button_sync_action():
    parse_html_sync()
    update_otbor_table()

def button_async_action():
    asyncio.run(parse_html_async())
    update_otbor_table()

result_label = Label(root, text='Выберите дату отбора')
result_label.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

otbor_table = ttk.Treeview(root, columns=('CatalogID', 'DateCreated', 'TotalProducts'), show='headings')
otbor_table.heading('CatalogID', text='ID Каталога')
otbor_table.heading('DateCreated', text='Дата')
otbor_table.heading('TotalProducts', text='Продукты')
otbor_table.column("#1", stretch=NO, width=75)
otbor_table.column("#2", stretch=YES, width=100)
otbor_table.column("#3", stretch=NO, width=100)
otbor_table.grid(row=2, column=0, padx=5, pady=5, sticky='NSEW')

otbor_table.bind('<<TreeviewSelect>>', on_catalog_select)

products_table = ttk.Treeview(root, columns=('CatalogID', 'Name', 'Price'), show='headings')
products_table.heading('CatalogID', text='ID Каталога')
products_table.heading('Name', text='Название гитары')
products_table.heading('Price', text='Цена')
products_table.column("#1", stretch=NO, width=75)
products_table.column("#2", stretch=YES, width=100)
products_table.column("#3", stretch=NO, width=100)
products_table.grid(row=2, column=1, padx=5, pady=5, sticky='NSEW')

update_otbor_table()

button_sync_label = Label(root, text='Собрать данные синхронно')
button_sync_label.grid(row=3, column=0)
button_sync = Button(root, text='Запуск', command=button_sync_action)
button_sync.grid(row=4, column=0, sticky=NSEW)

button_async_label = Label(root, text='Собрать данные асинхронно')
button_async_label.grid(row=3, column=1)
button_async = Button(root, text='Запуск', command=button_async_action)
button_async.grid(row=4, column=1, sticky=NSEW)

root.mainloop()