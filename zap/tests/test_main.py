import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By

link = 'https://zap.by/accumulator'

@pytest.fixture(scope='function')
def browser():
    browser = webdriver.Chrome()
    yield browser
    browser.quit()

def test_logo(browser):
    browser.get(link)
    elem_img = browser.find_element(By.CSS_SELECTOR, 'div.nheader__logo img')
    elem_img_attr = elem_img.get_attribute('alt')

    assert elem_img_attr == 'Zap.by', 'не найденно'

def test_cat_title(browser):
    browser.get(link)
    elem = browser.find_element(By.CSS_SELECTOR, 'div.container h1').text

    assert elem == 'Автомобильные аккумуляторы', 'не найденно'

def test_feauturebox_elem(browser):
    browser.get(link)
    elem = browser.find_element(By.CSS_SELECTOR, 'a.feature-box')

    assert elem, 'не найденно'

def test_items(browser):
    browser.get(link)
    elems = browser.find_elements(By.CSS_SELECTOR, 'div.product-block')

    assert len(elems) == 30, 'не найденно'

# def test_burgers_present(browser):
#     browser.get(link)
#     burgers = browser.find_elements(By.CSS_SELECTOR, 'div.LGqMD')

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