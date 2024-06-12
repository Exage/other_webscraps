import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By

url = 'https://atlantshop.by/catalog/refrigerators/'

@pytest.fixture(scope='function')
def browser():
    browser = webdriver.Chrome()
    yield browser
    browser.quit()

def test_page_title(browser):
    browser.get(url)
    elem = browser.find_element(By.CSS_SELECTOR, 'h1.l-main__title')

    assert elem.text == 'Холодильники ATLANT', 'Ошибка!'

def test_logo_alt(browser):
    browser.get(url)
    elem = browser.find_element(By.CSS_SELECTOR, 'a.b-header-logo img')

    assert elem.get_attribute('alt') == 'Сеть салонов-магазинов ATLANT', 'Ошибка!'

@pytest.mark.parametrize('pages', [ f'https://atlantshop.by/catalog/refrigerators/?PAGEN_1={i}' for i in range(1, 6) ])
def test_pages(browser, pages):
    new_link = pages
    browser.get(new_link)
    assert len(browser.find_elements(By.CSS_SELECTOR, 'article.product-cat')) == 16, 'Нет нужного количества товаров'