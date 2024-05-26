from bs4 import BeautifulSoup
import requests

from send_to_db import send_to_db

def sync_webscrap(urls):
    
    books = []

    for url in urls:
        page = requests.get(url)
        soup = BeautifulSoup(page.text, 'html.parser')

        products = soup.find_all('article', 'product-card')

        for product in products:
            title = product.find('div', 'product-title__head').text.strip() # Получить название товара
            author = product.find('div', 'product-title__author').text.strip() # Получить автора товара
            price = product.get('data-chg-product-price') # Получить прайс товара

            # Рассчитываем рейтинг товара
            rating = -1

            rating_wrapper = product.find('div', 'star-rating') # Найти блок со звездочками

            # Здесь идет проверка есть ли в блоке со звездочками блок с классом 'no-rating', если он будет, то в объект будет идти значение рейтинга товара -1
            if not rating_wrapper.find('div', 'no-rating'):
                # Если все же программа не нашла этот блок, то выполняются следующие действия
                rating = 0

                stars = rating_wrapper.find_all('svg') # Получить все символы звездочек

                # Тут будет сложно, но попробуй понять
                # У каждого симола со звездочками может быть до трех классов, а именно: 'star-rating-edit__item', 'star-rating__item--active' и 'star-rating__item--half-active'
                # Прикол в том, что если зведочка полная (желтая), то у нее имеется три класса, описанные выше
                # Если половина звездочки, то тогда у нее два класса 'star-rating-edit__item' и 'star-rating__item--half-active'
                # Если зведочка пустая (серая), то класс один 'star-rating-edit__item'
                # Но чтобы не проверять наличие тех самых классов, которые приведены выше, я решил проверять их количество
                # То есть: 3 класс - полная
                # 2 класса - наполовину
                # 1 класс - пустая
                # Цикл ниже чекает каждую звездочку
                for star in stars:
                    stars_len = len(star['class']) # Здесь мы получаем количество классов
                    
                    # Здесь срабатывает проверка, которую я уложил в одну строку (сорян, но так красивее).
                    # Если количество классов равно трем, то к переменной rating надо прибавить 1, если класса два, то прибавить 0.5, если класс один, то прибавить 0
                    rating += 1 if stars_len == 3 else 0.5 if stars_len == 2 else 0 
    
            # В итоге полученные данные мы заносим в словарь
            books.append({ 'title': title, 'author': author, 'price': int(price), 'rating': rating })
    
    # И в конечном итоге полученные данные мы заносим в Базу Данных
    send_to_db(books)

        