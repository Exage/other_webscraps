from asyncio import run

from tkinter import *
from tkinter import ttk

from db import init_db, fetch_all_products, fetch_products_by_selection, fetch_all_selections
from get_data import synchronously, asynchronously

def update_dates():
    selections = fetch_all_selections()

    for children in tree_dates.get_children():
        tree_dates.delete(children)

    for selection in selections:
        value = (selection[0], selection[1], selection[2])
        tree_dates.insert('', END, values=value)

def on_items_tree_click(event):
    item = tree_dates.focus()
    item_values = tree_dates.item(item, "values")

    if item_values:
        products = fetch_products_by_selection(int(item_values[0]))

        for children in tree_products.get_children():
            tree_products.delete(children)

        for product in products:
            value = (product[0], product[1], product[2])
            tree_products.insert('', END, values=value)

def show_all_products():
    products = fetch_all_products()

    for children in tree_products.get_children():
        tree_products.delete(children)

    for product in products:
        value = (product[0], product[1], product[2])
        tree_products.insert('', END, values=value)

def run_sync_webscrap():
    synchronously()
    update_dates()

def run_async_webscrap():
    run(asynchronously())
    update_dates()

init_db()

root = Tk()
root.title("Parser")
root.geometry("800x800")
root.minsize(400,500)

root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)
root.rowconfigure(1, weight=1)

columns_dates = ('parsing_number', 'date', 'numb_of_products')
 
tree_dates = ttk.Treeview(columns=columns_dates, show="headings")
tree_dates.grid(row=0, column=0, pady=5, sticky='nsew', columnspan=2)

tree_dates.heading("parsing_number", text="№ отбора")
tree_dates.heading("date", text="Дата")
tree_dates.heading("numb_of_products", text="Количесвто товаров")

tree_dates.column("#1", stretch=NO, width=75)
tree_dates.column("#2", stretch=YES, width=100)
tree_dates.column("#3", stretch=YES, width=100)

update_dates()

tree_dates.bind("<ButtonRelease-1>", on_items_tree_click)

columns_products = ('parsing_number', 'name', 'price')
 
tree_products = ttk.Treeview(columns=columns_products, show="headings")
tree_products.grid(row=1, column=0, sticky='nsew', columnspan=2)

tree_products.heading("parsing_number", text="№ отбора")
tree_products.heading("name", text="Название товара")
tree_products.heading("price", text="Цена")

tree_products.column("#1", stretch=NO, width=75)
tree_products.column("#2", stretch=YES, width=100)
tree_products.column("#3", stretch=NO, width=200)

btn_async = Button(root, command=show_all_products, text='Показать все товары')
btn_async.grid(row=2, column=0, padx=5, pady=0, columnspan=2, sticky='nsew')
label_title = Label(root, text='Выбери тип парсинга')
label_title.grid(row=3, column=0, columnspan=2, padx=5, pady=10)

btn_sync = Button(root, command=run_sync_webscrap, text='синхронный')
btn_sync.grid(row=4, column=0, padx=5, pady=5, sticky='nsew')

btn_async = Button(root, command=run_async_webscrap, text='асинхронный')
btn_async.grid(row=4, column=1, padx=5, pady=5, sticky='nsew')

root.mainloop()