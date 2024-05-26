from tkinter import *
from tkinter import ttk

import asyncio
from sql import get_data_tables, get_products_by_number
from get_data import sync_parsing, async_parsing

def show_dates():
    datas_table = get_data_tables()

    listbox.delete(0, END)

    for data in datas_table:    
        listbox.insert(END, f"{data[0]}. | {data[1]} | {data[2]}")

def selected(event):
    index = listbox.curselection()[0] + 1
    show_products(index)

def show_products(number):
    products = get_products_by_number(number)

    for children in tree.get_children():
        tree.delete(children)

    for product in products:
        value = (product[0], product[1], product[2], product[3])
        tree.insert('', END, values=value)

def sync_comand():
    sync_parsing()
    show_dates()

def async_comand():
    asyncio.run(async_parsing())
    show_dates()

root = Tk()
root.title("123")
root.geometry("1200x600")
root.minsize(700,400)

root.columnconfigure(2, weight=1)
root.rowconfigure(2, weight=1)

# Buttons

btn_sync_label = ttk.Label(text='Синхронно: ', anchor='w')
btn_sync_label.grid(row=0, column=0, sticky='nsew')

btn_async_label = ttk.Label(text='Асинхронно: ', anchor='w')
btn_async_label.grid(row=1, column=0, sticky='nsew')

btn_sync = Button(root, command=sync_comand, text='запуск')
btn_sync.grid(row=0, column=1, sticky='nsew')

btn_async = Button(root, command=async_comand, text='запуск')
btn_async.grid(row=1, column=1, sticky='nsew')

# Dates

listbox = Listbox(root)
listbox.grid(column=0, row=2, sticky="nsew", columnspan=2)

show_dates()

listbox.bind("<<ListboxSelect>>", selected)

# Products

columns_products = ('id', 'parsing_number', 'name', 'price')
 
tree = ttk.Treeview(columns=columns_products, show="headings")
tree.grid(column=2, row=0, sticky='nsew', rowspan=3)

tree.heading("id", text="Id")
tree.heading("parsing_number", text="номер отбора")
tree.heading("name", text="Название")
tree.heading("price", text="Цена")

tree.column("#1", stretch=NO, width=50)
tree.column("#2", stretch=NO, width=100)
tree.column("#3", stretch=YES, width=200)
tree.column("#4", stretch=NO, width=100)

root.mainloop()