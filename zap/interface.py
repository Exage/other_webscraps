from tkinter import *
from tkinter import ttk
from sql import get_products, get_selections, get_products_by_num

def build_interface(sync_def, async_def):
    root = Tk()
    root.title('Да')

    root.columnconfigure(0, weight=1)
    root.columnconfigure(1, weight=1)
    root.rowconfigure(2, weight=1)

    button_sync_data = Button(root, text='Получить данные синхронно', command=sync_def)
    button_sync_data.grid(row=0, column=0, pady=15, sticky=EW)

    button_async_data = Button(root, text='Получить данные асинхронно', command=async_def)
    button_async_data.grid(row=0, column=1, pady=15, sticky=EW)

    # Таблица отбора
    global tree_selection
    label_selection_table = Label(root, text='Таблица отбора')
    tree_selection = ttk.Treeview(root, columns=('SelectionID', 'SelectionDate', 'NumberOfProducts'), show='headings')
    label_selection_table.grid(row=1, column=0, padx=5)
    tree_selection.heading('SelectionID', text='ID')
    tree_selection.heading('SelectionDate', text='Дата')
    tree_selection.heading('NumberOfProducts', text='Продукты')
    tree_selection.grid(row=2, column=0, padx=5, sticky=NS)

    tree_selection.bind('<<TreeviewSelect>>', on_selection_select)

    show_table_selections()

    # Таблица товаров
    global tree_products
    label_products_table = Label(root, text='Таблица продуктов')
    tree_products = ttk.Treeview(root, columns=('SelectionID', 'ProductName', 'ProductArticle', 'ProductPrice', 'ProductBrand'), show='headings')
    label_products_table.grid(row=1, column=1, padx=5)
    tree_products.heading('SelectionID', text='ID отбора')
    tree_products.heading('ProductName', text='Название')
    tree_products.heading('ProductArticle', text='Артикул')
    tree_products.heading('ProductPrice', text='Цена')
    tree_products.heading('ProductBrand', text='Бренд')
    tree_products.grid(row=2, column=1, padx=5, sticky=NS)

    button_showall = Button(root, text='Показать все продукты', command=handle_showall_btn)
    button_showall.grid(row=3, column=0, columnspan=2, pady=15, sticky=EW)

    show_table_products()

    root.mainloop()

def show_table_products(num=0):
    products = get_products_by_num(num) if int(num) > 0 else get_products()
    
    for children in tree_products.get_children():
        tree_products.delete(children)
    for product in products:
        id, name, article, price, brand = product
        value = (id, name, article, price, brand)
        tree_products.insert('', END, values=value)

def on_selection_select(event):
    selected_item = tree_selection.selection()
    if selected_item:
        item_values = tree_selection.item(selected_item[0], 'values')

        show_table_products(item_values[0])

def show_table_selections():
    selections = get_selections()

    for children in tree_selection.get_children():
        tree_selection.delete(children)
    for selection in selections:
        id, name, price = selection
        value = (id, name, price)
        tree_selection.insert('', END, values=value)

def handle_showall_btn(*event):
    show_table_products()