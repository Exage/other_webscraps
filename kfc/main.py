import tkinter as tk
from tkinter import ttk

from handle_sql import get_selections_table, get_products_table, get_products_item, make_db
from get_products import get_products
from get_data import get_data

root = tk.Tk()
root.geometry("1200x800")
root.title("111")

make_db()

def show_text():
    text_window = tk.Toplevel(root)
    text_window.title("Текстовое окно")

    text_variable = get_data()
    
    text_area = tk.Text(text_window, wrap=tk.WORD)
    text_area.insert(tk.END, text_variable)
    text_area.configure(state='disabled')
    
    scrollbar = tk.Scrollbar(text_window, command=text_area.yview)
    text_area['yscrollcommand'] = scrollbar.set
    
    text_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

def update_table_1():
    dates = get_selections_table()

    for children in tree1.get_children():
        tree1.delete(children)

    for date in dates:
        value = (date[0], date[1], date[2])
        tree1.insert('', tk.END, values=value)

def update_table_2(products=None):
    if products is None:
        products = get_products_table()

    for children in tree2.get_children():
        tree2.delete(children)

    for product in products:
        value = (product[0], product[1], product[2])
        tree2.insert('', tk.END, values=value)

def parsing_s():
    get_products()
    update_table_1()
    update_table_2()

def on_item_select(event):
    selected_item = tree1.selection()[0]
    if selected_item:
        item_id = tree1.item(selected_item, "values")[0]
        products = get_products_item(item_id)
        update_table_2(products)

frame1 = tk.Frame(root)
frame1.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

label1 = tk.Label(frame1, text="Даты")
label1.pack()

tree1 = ttk.Treeview(frame1, columns=("id", "dates", "numb"), show="headings")
tree1.heading("id", text="ID")
tree1.heading("dates", text="Дата")
tree1.heading("numb", text="Продукты")
tree1.pack(fill=tk.BOTH, expand=True)

tree1.bind("<<TreeviewSelect>>", on_item_select)

for col in tree1["columns"]:
    tree1.column(col, width=100, minwidth=100, stretch=True)

update_table_1()

frame2 = tk.Frame(root)
frame2.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

label2 = tk.Label(frame2, text="Продукты")
label2.pack()

tree2 = ttk.Treeview(frame2, columns=("id", "name", "price"), show="headings")
tree2.heading("id", text="ID")
tree2.heading("name", text="Название")
tree2.heading("price", text="Цена")
tree2.pack(fill=tk.BOTH, expand=True)

for col in tree2["columns"]:
    tree2.column(col, width=100, minwidth=100, stretch=True)

update_table_2()

button_frame = tk.Frame(root)
button_frame.pack(fill=tk.X, pady=10)

button1 = tk.Button(button_frame, text="Получить продукты", command=parsing_s)
button1.pack(side=tk.LEFT, padx=5)

button2 = tk.Button(button_frame, text="Показать текст", command=show_text)
button2.pack(side=tk.RIGHT, padx=5)

root.mainloop()