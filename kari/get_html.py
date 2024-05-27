import asyncio
import aiohttp
import requests
from bs4 import BeautifulSoup
import datetime

from links import url_main, urls
from database import insert_parsing, insert_results

def handle_html(html):
    shop_items = html.find_all('article', 'shop_item')

    products = []

    for item in shop_items:

        item_info = item.find('a', 'gtmProductClick')

        product_name = item_info.get('data-name')
        product_article = item_info.get('data-model')
        product_brand = item_info.get('data-brand')
        product_price = item_info.get('data-price')
        product_url = f'{url_main}{item_info.get('data-url')}'

        products.append([product_name, product_article, product_brand, product_price, product_url])

    return products

def get_html_sync():
    
    items = []
    
    for url in urls:
        request = requests.get(url=url)
        soup = BeautifulSoup(request.text, 'lxml')

        items.extend(handle_html(soup))

    date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    parsing_id = insert_parsing(date, len(items))

    insert_results(parsing_id, items)

async def get_html_async():
    
    items = []

    for url in urls:
        async with aiohttp.ClientSession() as session:
            async with session.get(url=url, ssl=False) as response:
                soup = BeautifulSoup(await response.text(), 'lxml')
                
                items.extend(handle_html(soup))

    date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    parsing_id = insert_parsing(date, len(items))

    insert_results(parsing_id, items)