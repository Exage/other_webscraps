import aiohttp
import requests
from bs4 import BeautifulSoup

from database import insert_data

import json

main_url = 'https://burger-king.by'
urls = [
    'burgery-iz-govyadiny',
    'burgery-iz-kuricy-i-ryby'
]

def parse_burgers(soup):
    json_data = json.loads(soup.select_one('script[type="application/json"]').text)
    menu_string = json.loads(json_data['props']['pageProps']['initialState'])
    menu_dict = menu_string['menu']

    menu_items = []

    for menu_item in menu_dict['menu']:

        category = menu_item['category'] 

        if category['url'] in urls:

            for item in category['menuItems']:
                data = item.get('menuItemData')[0]
                price = item.get('price')
                name = data['name']
                description = data['marketingDescription']

                menu_items.append([ name, description, price ])

    insert_data(len(menu_items), menu_items)

def synchronously():
    page = requests.get(main_url)
    soup = BeautifulSoup(page.text, 'html.parser')

    parse_burgers(soup)

async def asynchronously():
    async with aiohttp.ClientSession() as session:
        async with session.get(url=main_url, ssl=False) as response:
            soup = BeautifulSoup(await response.text(), 'html.parser')
            
            parse_burgers(soup)