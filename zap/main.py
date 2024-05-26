import aiohttp
import asyncio
from requests_html import HTMLSession
from bs4 import BeautifulSoup

from sql import insert_data
from interface import build_interface, show_table_products, show_table_selections

links = [ f'https://zap.by/accumulator?page={i}' for i in range(1, 6) ]

def remove_words(x) -> str:
    str_1 = 'Автомобильные аккумуляторы'
    str_2 = 'Мотоциклетный аккумулятор'
    str_3 = 'Автомобильный аккумулятор'

    return x.text.replace(str_1, '').replace(str_2, '').replace(str_3, '').strip()

def convert_float(x) -> float:
    return float(x.text[:-3])

def find_strong(x):
    return x.find('strong').text

def get_products_data(soup) -> list:
    titles = list(map(lambda x: remove_words(x), soup.find_all('span', 'td-info-name_inner')))
    prices = list(map(lambda x: convert_float(x), soup.find_all('div', 'td-register-price')))
    brands = list(map(lambda x: find_strong(x), soup.find_all('div', 'td-info-brand')))
    articles = list(map(lambda x: find_strong(x.find('div', 'font-14')), soup.find_all('div', 'td-info-main')))

    return list(zip(titles, articles, prices, brands))

def sync_session(link) -> list:
    session = HTMLSession()
    r = session.get(link)

    soup = BeautifulSoup(r.text, 'html.parser')
    
    return get_products_data(soup)

async def async_session(url) -> list:
    async with aiohttp.ClientSession() as session:
        async with session.get(url=url, ssl=False) as response:
            soup = BeautifulSoup(await response.text(), 'lxml')

            return get_products_data(soup)

async def start_async_session():
    result = [ item for link in links for item in await async_session(link) ]
    insert_data(result)
    show_table_selections()
    show_table_products()

def run_async_session():
    asyncio.run(start_async_session())

def start_sync_session():
    result = [ item for link in links for item in sync_session(link) ]
    insert_data(result)
    show_table_selections()
    show_table_products()

if __name__ == '__main__':
    build_interface(start_sync_session, run_async_session)