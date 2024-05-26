import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By

import time

link = 'https://xistore.by/catalog/telefony/'

@pytest.fixture(scope='function')
def browser():
    browser = webdriver.Chrome()
    yield browser
    browser.quit()

def test_catalog_title(browser):
    browser.get(link)
    catalog_title = browser.find_element(By.CSS_SELECTOR, 'div.wysiwyg').text

    assert catalog_title == 'Смартфоны'

def test_burgers_present(browser):
    browser.get(link)
    category_link = browser.find_elements(By.CSS_SELECTOR, 'a.categoryList--item')

    assert len(category_link) > 0

def test_single_page(browser):
    browser.get(link)
    products = browser.find_elements(By.CSS_SELECTOR, 'div.search__page_item')
    assert len(products) == 20

def test_load_more(browser):
    browser.get(link)

    for _ in range(0, 3):
        load_more_btn = browser.find_element(By.CSS_SELECTOR, 'a.show-more__btn')
        load_more_btn.click()

        # Если ты будешь это запускать в универе, то поставь таймер на 10 и больше
        time.sleep(3)
    
    items = browser.find_elements(By.CSS_SELECTOR, 'div.search__page_item')

    assert len(items) == 73