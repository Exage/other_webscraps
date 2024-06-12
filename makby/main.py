import asyncio
import aiohttp
from bs4 import BeautifulSoup
import requests

from tkinter import *
from tkinter import ttk

from database import insert_data, get_selections, get_products_by_num

links = [ 
    'https://mak.by/catalog/burgery/',
    'https://mak.by/catalog/napitki/',
    'https://mak.by/catalog/mak-cafe/'
]

def parse_page(soup):

    section = soup.find('section', 'section-menu-content')
    containers = section.find_all('div', 'container')
    items_handled = list()

    for container in containers:

        if container.find('h2', 'subtitle'):
            category = container.find('h2', 'subtitle') 
        else:
            category = soup.select_one('h1.menu-title span')
        
        names = container.find_all('div', 'category__label')
        prices = container.find_all('div', 'category__price')
        
        products = [ [name.text.strip(), price.text.strip(), category.text.strip()] for name, price in zip(names, prices) ]

        items_handled.extend(products)

    return items_handled


def parse_page_sync():
    items_handled = list()

    for link in links:
        page = requests.get(link)
        soup = BeautifulSoup(page.text, 'html.parser')

        items_handled.extend(parse_page(soup))

    items_handled_len = len(items_handled)

    insert_data(items_handled_len, items_handled)

    load_listbox()


async def parse_page_async():

    items_handled = list()

    for link in links:
        async with aiohttp.ClientSession() as session:
            async with session.get(url=link, ssl=False) as response:
                soup = BeautifulSoup(await response.text(), 'html.parser')

                items_handled.extend(parse_page(soup))

    items_handled_len = len(items_handled)
    insert_data(items_handled_len, items_handled)
    load_listbox()

listbox_list = []
index = -1

def load_listbox():
    dates_table = get_selections()

    listbox.delete(0, END)

    for data in dates_table:
        listbox.insert(END, f'{data[0]}. {data[1]} - {data[2]}')

def load_tree(*args):
    products = get_products_by_num(index)

    for children in tree.get_children():
        tree.delete(children)

    for product in products:
        value = (product[0], product[1], product[2], product[3])
        tree.insert('', END, values=value)

def selected(event):
    global index
    index = listbox.curselection()[0] + 1
    load_tree()

def start_async_paring():
    asyncio.run(parse_page_async())

root = Tk()
root.title('Mak.by Parser')
root.geometry('800x700')
root.minsize(300, 300)

label_selections = Label(root, text='Выберите тип парсинга', font=('Montserrat', 14))
label_selections.pack()

btn_init = Button(root, text='синхронный', command=parse_page_sync)
btn_init.pack(fill=X, padx=5)

btn_clear = Button(root, text='асинхронный', command=start_async_paring)
btn_clear.pack(fill=X, padx=5)

label_selections = Label(root, text='Отборы')
label_selections.pack()

listbox = Listbox(root, width=35)
listbox.pack(fill=X)

load_listbox()

listbox.bind('<<ListboxSelect>>', selected)

label_selections = Label(root, text='Продукты')
label_selections.pack()

columns = ('SelectionID', 'ProductName', 'ProductPrice', 'ProductCategory')

tree = ttk.Treeview(columns=columns, show='headings')
tree.pack(fill=BOTH, expand=1)

tree.heading('SelectionID', text='id')
tree.heading('ProductName', text='название продукта')
tree.heading('ProductPrice', text='цена продукта')
tree.heading('ProductCategory', text='категория')

tree.column('#1', stretch=NO, width=70)
tree.column('#2', stretch=YES, width=150)
tree.column('#3', stretch=NO, width=120)
tree.column('#4', stretch=NO, width=150)

load_listbox()

root.mainloop()