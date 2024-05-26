from bs4 import BeautifulSoup

def parse_html(html):

    phones = list()

    names = list(map(lambda x: x.text, html.find_all('a', 'search__page_item-name')))
    prices = list(map(lambda x: x.text, html.find_all('span', 'super__price')))

    for name, price in zip(names, prices):
        
        show_name = name.replace('Смартфон', '').strip()
        show_price = price if price else 'Нет в наличии'
        
        phones.append([show_name, show_price])

    return phones