from parsing.handle_html import handle_html
from db import push_to_db
from links import urls

import aiohttp
import requests
from bs4 import BeautifulSoup

def get_html_sync(url):
    request = requests.get(url=url)
    soup = BeautifulSoup(request.text, 'lxml')
    return soup

async def get_html_async(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url=url, ssl=False) as response:
            soup = BeautifulSoup(await response.text(), 'lxml')
            return soup

def handle_items_sync():
    items = []
    
    for url in urls:
        html = get_html_sync(url)
        items.extend(handle_html(html, url))

    push_to_db(items, 'Синхронно')

    # with open('sync_res.txt', 'w') as f:
    #     f.write(str(datetime.datetime.now()))
    #     f.write('\n')
    #     for item in items:
    #         f.write(str(item))
    #         f.write('\n')

async def handle_items_async():
    items = []
    
    for url in urls:
        html = await get_html_async(url)
        items.extend(handle_html(html, url))

    push_to_db(items, 'Асинхронно')
    
    # with open('async_res.txt', 'w') as f:
    #     f.write(str(datetime.datetime.now()))
    #     f.write('\n')
    #     for item in items:
    #         f.write(str(item))
    #         f.write('\n')