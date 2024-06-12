import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By

items_per_page = 15
link = 'https://guitarland.by/catalog/katalog-gitar/bas-gitary/bas-gitary-cort/results.html'

@pytest.fixture(scope='function')
def browser():
    browser = webdriver.Chrome()
    yield browser
    browser.quit()

def test_get_title(browser):
    browser.get(link)
    title = browser.find_element(By.CSS_SELECTOR, 'div.art-postcontent h1')

    assert title.text == 'Бас-гитары Cort', 'Неправильный заголовок'

def test_address_1(browser):
    browser.get(link)
    address = browser.find_element(By.CSS_SELECTOR, 'div.contacts')

    assert address.text.find('Мулявина 3') != -1, 'Адрес не найден'

def test_address_2(browser):
    browser.get(link)
    address = browser.find_element(By.CSS_SELECTOR, 'div.contacts')

    assert address.text.find('ТЦ "Немига 3"') != -1, 'Адрес не найден'

@pytest.mark.parametrize('pages', [ f'{link.replace('results.html', f'results,{i * items_per_page}-{(i + 1) * items_per_page}.html')}' for i in range(0, 3) ])
def test_pages(browser, pages):
    new_link = pages
    browser.get(new_link)

    products = browser.find_elements(By.CSS_SELECTOR, 'div.product')

    assert len(products) > 0, 'Нет нужного количества товаров'