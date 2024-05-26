import asyncio
from parsing.soup import handle_items_sync, handle_items_async
from db import get_dates_from_db, get_items_from_db, get_item_from_db

from tkinter import *
from tkinter import ttk

import webbrowser

def load_listbox():
    datas_table = get_dates_from_db()

    listbox.delete(0, END)

    for data in datas_table:    
        listbox.insert(END, f"{data[0]}. | {data[1]} | {data[2]} | {data[3]}")

def load_tree(number):
    products = get_items_from_db(number)

    for children in tree.get_children():
        tree.delete(children)

    for product in products:
        value = (product[0], product[1], product[2], product[3], product[5])
        tree.insert('', END, values=value)

def selected(event):
    index = listbox.curselection()[0] + 1
    load_tree(index)

def on_double_click(event):
    item = tree.item(tree.focus())
    values = item['values']
    
    if values:
        id = values[0]
        link = get_item_from_db(id)[0][4]

        webbrowser.open(link)

def start_sync():
    print('Работает синхронный парсинг...')
    btn_sync.config(state=DISABLED)
    btn_async.config(state=DISABLED)
    
    try:
        handle_items_sync()
    finally:
        btn_sync.config(state=NORMAL)
        btn_async.config(state=NORMAL)
        load_listbox()

def enable_buttons():
    btn_sync.config(state="normal")
    btn_async.config(state="normal")

def disable_buttons():
    btn_sync.config(state="disabled")
    btn_async.config(state="disabled")

def start_sync():
    print('Работает синхронный парсинг...')
    disable_buttons()
    handle_items_sync()
    load_listbox()
    enable_buttons()

def start_async():
    print('Работает асинхронный парсинг...')
    disable_buttons()
    asyncio.run(handle_items_async())
    load_listbox()
    enable_buttons()

root = Tk()
root.geometry("1200x600")
root.minsize(700,400)

root.columnconfigure(2, weight=1)
root.rowconfigure(2, weight=1)

# Buttons

btn_sync_label = ttk.Label(text='Синхронно: ', anchor='w')
btn_sync_label.grid(row=0, column=0, sticky='nsew')

btn_async_label = ttk.Label(text='Асинхронно: ', anchor='w')
btn_async_label.grid(row=1, column=0, sticky='nsew')

btn_sync = Button(root, command=start_sync, text='запуск')
btn_sync.grid(row=0, column=1, sticky='nsew')

btn_async = Button(root, command=start_async, text='запуск')
btn_async.grid(row=1, column=1, sticky='nsew')

# Dates

listbox = Listbox(root, width=35)
listbox.grid(column=0, row=2, sticky="nsew", columnspan=2)

load_listbox()

listbox.bind("<<ListboxSelect>>", selected)

# Products

columns_products = ('id', 'parsing_number', 'name', 'price', 'page')
 
tree = ttk.Treeview(columns=columns_products, show="headings")
tree.grid(column=2, row=0, sticky='nsew', rowspan=3)

tree.heading("id", text="Id")
tree.heading("parsing_number", text="Номер отбора")
tree.heading("name", text="Название")
tree.heading("price", text="Цена (BYN)")
tree.heading("page", text="Номер страницы")

tree.column("#1", stretch=NO, width=50)
tree.column("#2", stretch=NO, width=100)
tree.column("#3", stretch=YES, width=200)
tree.column("#4", stretch=NO, width=100)
tree.column("#5", stretch=NO, width=150)

tree.bind("<Double-1>", on_double_click)

root.mainloop()