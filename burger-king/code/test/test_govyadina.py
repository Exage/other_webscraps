import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By

link = 'https://burger-king.by/menu/burgery-iz-govyadiny/'

@pytest.fixture(scope='function')
def browser():
    browser = webdriver.Chrome()
    yield browser
    browser.quit()

def test_page_title(browser):
    browser.get(link)
    browser.find_element(By.CSS_SELECTOR, 'h2.deoUUJ').text == 'Бургеры из говядины'

def test_burgers_present(browser):
    browser.get(link)
    burgers = browser.find_elements(By.CSS_SELECTOR, 'div.LGqMD')

    assert len(burgers) > 0, 'Не найдено'

def test_burger_names(browser):
    browser.get(link)
    burger_names = browser.find_elements(By.CSS_SELECTOR, 'p.qJHVg')

    assert len(burger_names) > 0, 'Не найдено'
    for name in burger_names:
        assert name.text != '', 'Есть бургер без имени'

def test_burger_prices(browser):
    browser.get(link)
    burger_prices = browser.find_elements(By.CSS_SELECTOR, 'p.dNhVcj')

    assert len(burger_prices) > 0, 'Не найдено'

def test_burger_images(browser):
    browser.get(link)
    burger_images = browser.find_elements(By.CSS_SELECTOR, 'img.hoMPrH')
    
    assert len(burger_images) > 0, 'Не найдено'
    for img in burger_images:
        assert img.get_attribute('src') != '', 'Бургер без картинки'

# class TestBurgerKingMenu:
    
#     @pytest.fixture(scope='class', autouse=True)
#     def setup_class(self, browser_class):
#         self.browser = browser_class
#         self.browser.get('https://burger-king.by/menu/burgery-iz-govyadiny/')
    
#     def test_page_title(self):
#         assert 'Бургеры из говядины' in self.browser.title
    
#     def test_burgers_present(self):
#         burgers = self.browser.find_elements(By.CLASS_NAME, 'LGqMD')
#         assert len(burgers) > 0, 'No burgers found on the page'
    
#     def test_burger_names(self):
#         burger_names = self.browser.find_elements(By.CLASS_NAME, 'qJHVg')
#         assert len(burger_names) > 0, 'No burger names found on the page'
#         for name in burger_names:
#             assert name.text != '', 'Found a burger with no name'

#     def test_burger_prices(self):
#         burger_prices = self.browser.find_elements(By.CLASS_NAME, 'dNhVcj')
#         assert len(burger_prices) > 0, 'No burger prices found on the page'
#         for price in burger_prices:
#             assert price.text != '', 'Found a burger with no price'

#     def test_burger_images(self):
#         burger_images = self.browser.find_elements(By.CLASS_NAME, 'hoMPrH')
#         assert len(burger_images) > 0, 'No burger images found on the page'
#         for img in burger_images:
#             assert img.get_attribute('src') != '', 'Found a burger with no image source'
