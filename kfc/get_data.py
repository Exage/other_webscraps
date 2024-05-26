import aiohttp
import asyncio
from bs4 import BeautifulSoup

urls = [
    # { 
    #     'url': 'https://www.kfc.by/page/faq',
    #     'find': ['div.page-content']
    # },
    { 
        'url': 'https://www.kfc.by/page/our-contacts',
        'find': ['div.page-content']
    },
    { 
        'url': 'https://www.kfc.by/about-us',
        'find': ['span.flag', 'div.card-title', 'div.card-text']
    },
    { 
        'url': 'https://www.kfc.by/stores',
        'find': ['h5.card-title', 'p.address'],
        'limit': 3
    },
    # { 
    #     'url': 'https://www.kfc.by/news',
    #     'find': ['h5.card-title', 'div.card-subtitle'],
    #     'limit': 3
    # },
]

def write_data(items):
    page_content = ''

    for item in items:

        text = str(item.text).strip()

        page_content += text
        page_content += '\n'
    
    return page_content

async def get_data(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url=url, ssl=False) as response:
            soup = BeautifulSoup(await response.text(), 'html.parser')

            page_title = soup.find('title').text.replace(' | KFC.BY', '')
            section = soup.find('section', 'p-header')

            cards = section.find_all('div', 'card')

            return [page_title, cards]

async def parse_pages():
    
    page_content = ''

    for url_item in urls:
        url, find = url_item.values()

        title, cards = await get_data(url)
        page_content += (f'{title}\n')

        for card in cards:
            for i in find:
                print(i)

        # print(url)
        
        
        
        
    with open('index.html', 'w') as file:
        file.write(page_content)


asyncio.run(parse_pages())