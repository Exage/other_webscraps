import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By

link = "https://www.chitai-gorod.ru/"

@pytest.fixture(scope="function")
def browser():
    browser = webdriver.Chrome()
    yield browser
    browser.quit()

def test_get_logo(browser):
    browser.get(link)
    browser.find_element(By.CSS_SELECTOR, "svg.header-logo__icon")

def test_first_product(browser):
    browser.get(link)
    browser.find_element(By.CSS_SELECTOR, "article.product-card").get('data-chg-product-name') == 'Токийский гуль. Книга 1'

@pytest.mark.parametrize('pages', [ f'https://www.chitai-gorod.ru/catalog/books/manga-110064?page={i}' for i in range(1, 6) ])
def test_pages(browser, pages):
    new_link = pages
    browser.get(new_link)
    len(browser.find_elements(By.CSS_SELECTOR, "article.product-card")) == 48