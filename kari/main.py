import asyncio

import tkinter as tk
from tkinter import ttk

import webbrowser

from database import fetch_all_parsings, fetch_all_results, fetch_results_by_selection
from get_html import get_html_sync, get_html_async

def update_table1_data(data):
    for item in table1.get_children():
        table1.delete(item)
        
    for row in data:
        table1.insert('', 'end', values=row)

def update_table2_data(data):
    for item in table2.get_children():
        table2.delete(item)
        
    for row in data:
        values = (row[:6])
        table2.insert('', 'end', values=values)

def on_table1_item_click(event):
    selected_item = table1.selection()

    if selected_item:
        id = table1.item(selected_item[0])["values"][0]

        data = fetch_results_by_selection(id)

        update_table2_data(data)

def on_table2_item_click(event):
    selected_item = table2.selection()
    
    if selected_item:
        id = table2.item(selected_item[0])["values"][0]

        for data in initial_data_table2:
            if data[0] == id:
                webbrowser.open(data[6])

def button1_click():
    get_html_sync()

    data = fetch_all_parsings()
    update_table1_data(data)

def button2_click():
    asyncio.run(get_html_async())

    data = fetch_all_parsings()
    update_table1_data(data)

root = tk.Tk()
root.title('Tkinter Interface')

root.rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)

table1 = ttk.Treeview(root, columns=('ID_Parsing', 'Date', 'Items'), show='headings')
table1.heading('ID_Parsing', text='ID Парсинга')
table1.heading('Date', text='Дата')
table1.heading('Items', text='Предметы')
table1.grid(row=0, column=0, padx=10, pady=10, sticky='NSEW')

table1.bind('<ButtonRelease-1>', on_table1_item_click)

table2 = ttk.Treeview(root, columns=('ID', 'ID_Parsing', 'Name', 'Article', 'Brand', 'Price'), show='headings')
table2.heading('ID', text='ID')
table2.heading('ID_Parsing', text='ID Парсинга')
table2.heading('Name', text='Название')
table2.heading('Article', text='Артикул')
table2.heading('Brand', text='Бренд')
table2.heading('Price', text='Цена')
table2.grid(row=0, column=1, padx=10, pady=10, sticky='NSEW')

table2.bind('<Double-1>', on_table2_item_click)

button1 = tk.Button(root, text='Синхронный отбор товаров', command=button1_click)
button1.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

button2 = tk.Button(root, text='Асинхронный отбор товаров', command=button2_click)
button2.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

initial_data_table1 = fetch_all_parsings()
initial_data_table2 = fetch_all_results()

update_table1_data(initial_data_table1)

root.mainloop()
