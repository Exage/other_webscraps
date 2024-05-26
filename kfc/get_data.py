import aiohttp
import asyncio
from bs4 import BeautifulSoup

from datetime import datetime

urls = [
    { 
        'url': 'https://www.kfc.by/about-us',
        'find': ['span.flag', 'div.card-title', 'div.card-text span']
    },
    { 
        'url': 'https://www.kfc.by/eleven-ingredients',
        'find': ['h5.card-title', 'div.card-text p']
    },
    {
        'url': 'https://www.kfc.by/stores',
        'find': ['h5.card-title', 'p.address', 'p.phone'],
    }
]

all_text_data = f'Дата получения данных {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n'

async def parse_page(url_item, soup, cards):
    find_elems = url_item['find']

    page_content = ''

    page_title = f'\n=== {soup.find('title').text.replace(' | KFC.BY', '')} ===\n\n\n'

    page_content += page_title

    for card in cards:
        for elem in find_elems:
            row_elem = card.select_one(elem)
            
            if row_elem:  
                row = row_elem.text.replace('    ', '').replace('\n', '')
                page_content += f'{row}\n'
        
        page_content += '\n'


    return page_content

async def parse_pages():

    global all_text_data

    for url_item in urls:
        url = url_item['url']
        async with aiohttp.ClientSession() as session:
            async with session.get(url=url, ssl=False) as response:
                soup = BeautifulSoup(await response.text(), 'html.parser')
                
                section = soup.find('section', 'p-header')
                cards = section.find_all('div', 'card')

                all_text_data += await parse_page(url_item, soup, cards)

    # Запись всех данных в файл
    # with open('index.txt', 'w', encoding='utf-8') as file:
    #     file.write(all_text_data)

def get_data():
    asyncio.run(parse_pages())
    print(all_text_data)
    return all_text_data