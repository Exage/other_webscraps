import aiohttp
from bs4 import BeautifulSoup
import requests
import lxml

import re
from datetime import datetime

from links import links
from sql import insert_into_data_table, insert_into_products_table

def sync_parsing():
    all_items = []

    for link in links:
        response = requests.get(url=link)
        soup = BeautifulSoup(response.text, 'lxml')

        products = soup.find_all('div', 'item')

        for product in products:
            product_name = product.find('div', 'link-wrap').find('a').text
            product_price = int(re.sub(r'\s+', '', product.find('mark', 'price').text[:-3]))
            
            all_items.append((product_name, product_price))
        
    cur_date = datetime.now().strftime('%Y-%m-%d')
    selection_id = insert_into_data_table(cur_date, len(all_items))
    
    for item in all_items:
        insert_into_products_table(selection_id, item[0], item[1])

async def async_parsing():
    all_items = []

    for link in links:
        async with aiohttp.ClientSession() as session:
            async with session.get(url=link) as response:
                soup = BeautifulSoup(await response.text(), 'lxml')
                products = soup.find_all('div', 'item')

                for product in products:
                    product_name = product.find('div', 'link-wrap').find('a').text
                    product_price = int(re.sub(r'\s+', '', product.find('mark', 'price').text[:-3]))
                    
                    all_items.append((product_name, product_price))

    cur_date = datetime.now().strftime('%Y-%m-%d')
    selection_id = insert_into_data_table(cur_date, len(all_items))
    
    for item in all_items:
        insert_into_products_table(selection_id, item[0], item[1])