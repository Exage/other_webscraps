from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time
from handle_sql import make_db, add_products, add_selection

company_url = 'https://www.kfc.by/menu'
categories_order = ['Комбо', 'Бургеры', 'Твистеры']

def get_products():
    driver = webdriver.Chrome()
    driver.get(company_url)
    driver.set_window_size(1400, 800)
    # time.sleep(10)
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # Явные ожидания до тех пор, пока не появятся продукты на странице (хз что это такое, я эти строчки нашел на просторах интернета)
    # wait = WebDriverWait(driver, 100)
    # wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'product')))

    cat_title = soup.find_all('div', 'product-list')

    # with open(f'result.html', 'w', encoding='utf-8') as file:
    #     for item in cat_title:
    #         file.write(f'{item}\n')

    filtered_products = []

    for i in categories_order:
        cat_title = soup.find('h2', 'card-title', string=i)
        cat_product_list = cat_title.find_next_sibling('div', 'product-list')
        
        cat_products = cat_product_list.find_all('div', 'product-row')

        for product in cat_products:
            name = product.find('h3', 'cat-title').text
            price = float(product.find('span', 'price').text.replace(',', '.'))

            filtered_products.append([name, price])
        
    add_products(len(filtered_products), filtered_products)

    driver.quit()