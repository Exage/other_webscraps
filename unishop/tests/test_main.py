import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By

link = "https://unishop.by/categories/diski/"

@pytest.fixture(scope="function")
def browser():
    browser = webdriver.Chrome()
    yield browser
    browser.quit()

def test_logo(browser):
    browser.get(link)
    browser.find_element(By.CSS_SELECTOR, "div.logo")

def test_check_cat_name(browser):
    browser.get(link)
    browser.find_element(By.CSS_SELECTOR, "div.hwrap h1") == 'Автомобильные диски'

@pytest.mark.parametrize('pages', [ f'https://unishop.by/categories/diski/={i}' for i in range(0, 5) ])
def test_pages(browser, pages):
    new_link = pages
    browser.get(new_link)
    len(browser.find_elements(By.CSS_SELECTOR, "article.product-card")) == 20