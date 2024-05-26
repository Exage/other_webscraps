import aiohttp
import asyncio
from bs4 import BeautifulSoup

from send_to_db import send_to_db

async def fetch_page(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url, ssl=False) as response:
            return await response.text()

async def async_parse(urls):
    
    books = []

    for url in urls:
        text = await fetch_page(url)
        soup = BeautifulSoup(text, 'html.parser')

        products = soup.find_all('article', 'product-card')

        for product in products:
            title = product.find('div', 'product-title__head').text.strip()
            author = product.find('div', 'product-title__author').text.strip()
            price = product.get('data-chg-product-price')

            rating = -1

            rating_wrapper = product.find('div', 'star-rating')

            if not rating_wrapper.find('div', 'no-rating'):
                rating = 0

                stars = rating_wrapper.find_all('svg')

                for star in stars:
                    stars_len = len(star['class'])
                    rating += 1 if stars_len == 3 else 0.5 if stars_len == 2 else 0 
    
            books.append({ 'title': title, 'author': author, 'price': int(price), 'rating': rating })
    
    send_to_db(books)

def async_webscrap(urls):
    asyncio.run(async_parse(urls))