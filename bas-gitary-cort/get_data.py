import asyncio
import aiohttp
from requests_html import HTMLSession
from bs4 import BeautifulSoup

from database import create_tables, add_products

items_per_page = 15
url = 'https://guitarland.by/catalog/katalog-gitar/bas-gitary/bas-gitary-cort/results.html'
urls = [ f'{url.replace('results.html', f'results,{i * items_per_page}-{(i + 1) * items_per_page}.html')}' for i in range(0, 3) ]

def parse_page(soup):

    guitars = list()
    products = soup.find_all('div', 'product')

    for product in products:
        name = product.select_one('div.vmzag a').text.strip()
        price = product.select_one('span.productPrice').text.strip()

        guitars.append([ name, price ])

    return guitars
        

def parse_html_sync():

    create_tables()

    guitars = []

    for url in urls:
        session = HTMLSession()
        r = session.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        products = parse_page(soup)

        guitars.extend(products)
    
    add_products(guitars)
    
async def parse_html_async():

    create_tables()

    guitars = []

    for url in urls:
        async with aiohttp.ClientSession() as session:
            async with session.get(url=url, ssl=False) as response:
                soup = BeautifulSoup(await response.text(), 'html.parser')
                products = parse_page(soup)

                guitars.extend(products)

    add_products(guitars)
