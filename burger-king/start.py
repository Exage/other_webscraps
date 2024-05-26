from asyncio import run

from tkinter import *
from tkinter import ttk

from database import get_products, get_selections
from get_burgers import synchronously, asynchronously

def update_table_products():
    products = get_products()

    for children in tree_products.get_children():
        tree_products.delete(children)

    for product in products:
        
        id = product[0]
        name = product[1]
        price = product[2]
        description = product[3] if product[3] else 'Нет описания'
        
        value = (id, name, price, description)
        tree_products.insert('', END, values=value)

def update_table_selections():
    selections = get_selections()

    for children in tree_selection.get_children():
        tree_selection.delete(children)

    for selection in selections:
        
        id = selection[0]
        name = selection[1]
        price = selection[2]
        
        value = (id, name, price)
        tree_selection.insert('', END, values=value)

def handle_update_btn():
    update_table_products()
    update_table_selections()

def run_async():
    run(asynchronously())

root = Tk()
root.title('ВК')

root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)
root.rowconfigure(7, weight=1)

button_sync_data = Button(root, text='Sync', width=20, command=synchronously)
button_sync_data.grid(row=3, column=0, columnspan=1, pady=5)

button_async_data = Button(root, text='Async', width=20, command=run_async)
button_async_data.grid(row=3, column=1, columnspan=1, pady=5)

# Таблица отбора
label_selection_table = Label(root, text='Selection Table')
label_selection_table.grid(row=4, column=0, columnspan=2, pady=10)
tree_selection = ttk.Treeview(root, columns=('SelectionID', 'SelectionDate', 'NumberOfProducts'), show='headings')
tree_selection.heading('SelectionID', text='SelectionID')
tree_selection.heading('SelectionDate', text='SelectionDate')
tree_selection.heading('NumberOfProducts', text='NumberOfProducts')
tree_selection.grid(row=5, column=0, columnspan=2, padx=5, pady=10)

update_table_selections()

# Таблица товаров
label_products_table = Label(root, text='Products Table')
label_products_table.grid(row=6, column=0, columnspan=2, pady=5)
tree_products = ttk.Treeview(root, columns=('SelectionID', 'ProductName', 'ProductPrice', 'ProductDescription'), show='headings')
tree_products.heading('SelectionID', text='SelectionID')
tree_products.heading('ProductName', text='ProductName')
tree_products.heading('ProductPrice', text='ProductPrice')
tree_products.heading('ProductDescription', text='ProductDescription')
tree_products.grid(row=7, column=0, columnspan=2, padx=5, pady=5, sticky=NS)

button_update_tables = Button(root, text='Update Tables', command=handle_update_btn)
button_update_tables.grid(row=8, column=0, columnspan=2, pady=5)

update_table_products()

root.mainloop()