import aiohttp
import requests
from bs4 import BeautifulSoup
from db import insert_selection, insert_product

from datetime import datetime

urls = [ f'https://atlantshop.by/catalog/refrigerators/?PAGEN_1={i}' for i in range(1, 6) ]

def parse_html(html):

    products = list()

    names = list(map(lambda x: x.text.strip(), html.find_all('h2', 'product-cat-title')))
    prices = list(map(lambda x: x.text.strip(), html.find_all('div', 'product-cat-price-current')))

    for name, price in zip(names, prices):
        price_handled = price if price else 'Нет в наличии'

        products.append((name, price_handled))

    return products


def synchronously():
    
    data = list()

    for url in urls:
        request = requests.get(url)
        soup = BeautifulSoup(request.text, 'html.parser')
        data.extend(parse_html(soup))

    selection_id = insert_selection(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), len(data))
    
    for item in data:
        insert_product(selection_id, *item)

async def asynchronously():

    data = list()

    for url in urls:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, ssl=False) as response:
                soup = BeautifulSoup(await response.text(), 'html.parser')
                data.extend(parse_html(soup))

    selection_id = insert_selection(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), len(data))

    for item in data:
        insert_product(selection_id, *item)