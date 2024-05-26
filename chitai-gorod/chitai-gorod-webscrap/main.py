from tkinter import *
from tkinter import ttk

from send_to_db import get_dates, get_products_by_number
from sync_webscrap import sync_webscrap
from async_webscrap import async_webscrap

urls = [ f'https://www.chitai-gorod.ru/catalog/books/manga-110064?page={url}' for url in range(1, 6)]

def update_dates():
    dates = get_dates()

    for children in tree_dates.get_children():
        tree_dates.delete(children)

    for date in dates:
        value = (date['parsing_number'], date['date'], date['numb_of_products'])
        tree_dates.insert('', END, values=value)

def on_items_tree_click(event):
    item = tree_dates.focus()
    item_values = tree_dates.item(item, "values")

    if item_values:
        books = get_products_by_number(int(item_values[0]))

        for children in tree_products.get_children():
            tree_products.delete(children)

        for book in books:
            parsing_number = book['parsing_number']
            title = book['title']
            author = book['author'] if book['author'] else 'Неизвестен'
            rating = book['rating'] if book['rating'] > 0 else 'Нет оценки'
            price = f'{book['price']} ₽'

            value = (parsing_number, title, author, price, rating)
            tree_products.insert('', END, values=value)

def run_sync_webscrap():
    sync_webscrap(urls=urls)
    update_dates()

def run_async_webscrap():
    async_webscrap(urls=urls)
    update_dates()

root = Tk()
root.title("Parser")
root.geometry("1000x600")
root.minsize(400,500)

root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)
root.rowconfigure(3, weight=1)

label_title = Label(root, text='Выбери тип парсинга')
label_title.grid(row=0, column=0, columnspan=2, padx=15, pady=0)

btn_sync = Button(root, command=run_sync_webscrap, text='синхронный')
btn_sync.grid(row=1, column=0, padx=15, pady=0, sticky='nsew')

btn_async = Button(root, command=run_async_webscrap, text='асинхронный')
btn_async.grid(row=1, column=1, padx=15, pady=0, sticky='nsew')

columns_dates = ('parsing_number', 'date', 'numb_of_products')
 
tree_dates = ttk.Treeview(columns=columns_dates, show="headings")
tree_dates.grid(row=2, column=0, pady=5, sticky='nsew', columnspan=2)

tree_dates.heading("parsing_number", text="№ отбора")
tree_dates.heading("date", text="Дата")
tree_dates.heading("numb_of_products", text="Количесвто товаров")

tree_dates.column("#1", stretch=NO, width=75)
tree_dates.column("#2", stretch=YES, width=100)
tree_dates.column("#3", stretch=YES, width=100)

update_dates()

tree_dates.bind("<Double-1>", on_items_tree_click)

columns_products = ('parsing_number', 'title', 'author', 'price', 'rating')
 
tree_products = ttk.Treeview(columns=columns_products, show="headings")
tree_products.grid(row=3, column=0, sticky='nsew', columnspan=2)

tree_products.heading("parsing_number", text="№ отбора")
tree_products.heading("title", text="Название товара")
tree_products.heading("author", text="Автор")
tree_products.heading("price", text="Цена")
tree_products.heading("rating", text="Рейтинг")

tree_products.column("#1", stretch=NO, width=75)
tree_products.column("#2", stretch=YES, width=100)
tree_products.column("#3", stretch=NO, width=200)
tree_products.column("#4", stretch=NO, width=100)
tree_products.column("#5", stretch=NO, width=100)

root.mainloop()