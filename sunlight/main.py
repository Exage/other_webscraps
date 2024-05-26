import asyncio
import aiohttp
from bs4 import BeautifulSoup
import requests


from tkinter import *
from tkinter import ttk

from database import insert_data, get_selections, get_products_by_num

links = [ f'https://sunlight.net/catalog/page-{i}/' for i in range(1, 6)]

def parse_page(soup):

    items = soup.select('div.cl-item')
    items_handled = list()

    for item in items:
        name = item.get('data-analytics-name')
        price = int(item.get('data-analytics-price'))
        brand = item.get('data-analytics-brand')

        items_handled.append([name, price, brand])

    return items_handled


def parse_page_sync():
    items_handled = list()

    for i, link in enumerate(links):
        page = requests.get(link)
        soup = BeautifulSoup(page.text, 'html.parser')

        items_handled.extend(parse_page(soup))

    items_handled_len = len(items_handled)
    insert_data(items_handled_len, items_handled)
    load_listbox()


async def parse_page_async():

    items_handled = list()

    for i, link in enumerate(links):
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
        listbox.insert(END, f"{data[0]}. {data[1]} - {data[2]}")

def load_tree(*args):
    print(index)
    if index > 0:
        products = get_products_by_num(index)

        for children in tree.get_children():
            tree.delete(children)

        for product in products:
            value = (product[0], product[1], product[2], product[3])
            tree.insert('', END, values=value)

def unload_tree(*args):
    if index > 0:
        for children in tree.get_children():
            tree.delete(children)

def selected(event):
    global index
    index = listbox.curselection()[0] + 1

def start_async_paring():
    asyncio.run(parse_page_async())

root = Tk()
root.title("Z")
root.geometry("1000x700")
root.minsize(300, 300)

label_selections = Label(root, text="Chose parsing type", font=("Montserrat", 14))
label_selections.pack()

btn_init = Button(root, text="Synchronously", command=parse_page_sync)
btn_init.pack(fill=X, padx=5)

btn_clear = Button(root, text="Asynchronously", command=start_async_paring)
btn_clear.pack(fill=X, padx=5)

label_selections = Label(root, text="Selections", font=("Montserrat", 14))
label_selections.pack()

listbox = Listbox(root, width=35)
listbox.pack(fill=X)

load_listbox()

listbox.bind("<<ListboxSelect>>", selected)

label_selections = Label(root, text="Products", font=("Montserrat", 14))
label_selections.pack()

btn_init = Button(root, text="Load", command=load_tree)
btn_init.pack(fill=X, padx=5)

btn_clear = Button(root, text="Unload", command=unload_tree)
btn_clear.pack(fill=X, padx=5)

columns = ("SelectionID", "ProductName", "ProductPrice", "ProductBrand")

tree = ttk.Treeview(columns=columns, show="headings")
tree.pack(fill=BOTH, expand=1)

tree.heading("SelectionID", text="SelectionID")
tree.heading("ProductName", text="ProductName")
tree.heading("ProductPrice", text="ProductPrice")
tree.heading("ProductBrand", text="ProductBrand")

tree.column("#1", stretch=NO, width=70)
tree.column("#2", stretch=YES, width=150)
tree.column("#3", stretch=NO, width=120)
tree.column("#4", stretch=YES, width=120)

load_listbox()

root.mainloop()