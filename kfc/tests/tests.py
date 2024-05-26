import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By

link = 'https://www.kfc.by/menu'

@pytest.fixture(scope='function')
def browser():
    browser = webdriver.Chrome()
    browser.set_window_size(1400, 800)
    yield browser
    browser.quit()

def test_check_items_num(browser):
    browser.get(link)
    elements = browser.find_elements(By.CSS_SELECTOR, 'div.categories')
    assert len(elements) == 18

def test_first_cat_title(browser):
    browser.get(link)
    elements = browser.find_elements(By.CSS_SELECTOR, 'h2.card-panel')
    assert elements[5].text == 'Комбо'

def test_second_cat_title(browser):
    browser.get(link)
    elements = browser.find_elements(By.CSS_SELECTOR, 'h2.card-panel')
    assert elements[6].text == 'Бургеры'

def test_third_cat_title(browser):
    browser.get(link)
    elements = browser.find_elements(By.CSS_SELECTOR, 'h2.card-panel')
    assert elements[7].text == 'Твистеры'

#     assert len(burgers) > 0, 'Не найдено'

# def test_burger_names(browser):
#     browser.get(link)
#     burger_names = browser.find_elements(By.CSS_SELECTOR, 'p.qJHVg')

#     assert len(burger_names) > 0, 'Не найдено'
#     for name in burger_names:
#         assert name.text != '', 'Есть бургер без имени'

# def test_burger_prices(browser):
#     browser.get(link)
#     burger_prices = browser.find_elements(By.CSS_SELECTOR, 'p.dNhVcj')

#     assert len(burger_prices) > 0, 'Не найдено'

# def test_burger_images(browser):
#     browser.get(link)
#     burger_images = browser.find_elements(By.CSS_SELECTOR, 'img.hoMPrH')
    
#     assert len(burger_images) > 0, 'Не найдено'
#     for img in burger_images:
#         assert img.get_attribute('src') != '', 'Бургер без картинки'