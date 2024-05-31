import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By

link = 'https://www.dom.by/gds/divany/brest/'

@pytest.fixture(scope='function')
def browser():
    browser = webdriver.Chrome()
    yield browser
    browser.quit()

def test_get_title(browser):
    browser.get(link)
    element = browser.find_element(By.CSS_SELECTOR, 'h1.GdsTitle')

    assert element.text == 'Диваны в Бресте — фото и цены', 'Неправильный заголовок'

def test_get_city(browser):
    browser.get(link)
    element = browser.find_element(By.CSS_SELECTOR, 'span.DropDown__text')
    
    assert element.text == 'Брест', 'Неправильный город'

@pytest.mark.parametrize('pages', [ f'https://www.dom.by/gds/divany/brest/?page={i}' for i in range(1, 6) ])
def test_pages(browser, pages):
    new_link = pages
    browser.get(new_link)
    assert len(browser.find_elements(By.CSS_SELECTOR, 'div.gdsItem__cart')) >= 30, 'Нет нужного количества товаров'