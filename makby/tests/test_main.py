import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By

link = 'https://mak.by/catalog/burgery/'

@pytest.fixture(scope='function')
def browser():
    browser = webdriver.Chrome()
    yield browser
    browser.quit()

def test_logo(browser):
    browser.get(link)

    logo = browser.find_element(By.CSS_SELECTOR, 'div.header-logo__icon')

    assert logo, 'что-то не то'

def test_cat_title(browser):
    browser.get(link)
    
    cat_title = browser.find_element(By.CSS_SELECTOR, 'h1.menu-title span')

    assert cat_title.text.strip() == 'Бургеры и Роллы', 'что-то не то'

@pytest.mark.parametrize('pages', [ 'burgery', 'napitki', 'mak-cafe' ])
def test_pages(browser, pages):
    new_link = f'https://mak.by/catalog/{pages}'
    browser.get(new_link)

    products = browser.find_elements(By.CSS_SELECTOR, 'a.category')

    assert len(products) > 0, 'что-то не то'

# def test_product_prices(browser):
#     browser.get(link)
#     product_prices = browser.find_elements(By.CSS_SELECTOR, ' div.cl-item-info-price-discount')
#     assert len(product_prices) > 0, 'что-то не то'
