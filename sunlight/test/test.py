import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By

link = 'https://sunlight.net/catalog/'

@pytest.fixture(scope='function')
def browser():
    browser = webdriver.Chrome()
    yield browser
    browser.quit()

def test_page_catalog_count(browser):
    browser.get(link)
    assert '28 186 товаров' in browser.find_element(By.CSS_SELECTOR, 'span.catalog-title__count').text

def test_products_count(browser):
    browser.get(link)
    products = browser.find_elements(By.CSS_SELECTOR, 'div.cl-item')
    assert len(products) == 65, 'что-то не то'

def test_product_brand(browser):
    browser.get(link)
    products = browser.find_elements(By.CSS_SELECTOR, 'div.cl-item')
    first_brand = products[0].find_element(By.CSS_SELECTOR, 'div.cl-item-info-brand').text
    assert first_brand == 'БРИЛЛИАНТЫ ЯКУТИИ', 'что-то не то'

def test_product_prices(browser):
    browser.get(link)
    product_prices = browser.find_elements(By.CSS_SELECTOR, ' div.cl-item-info-price-discount')
    assert len(product_prices) > 0, 'что-то не то'
