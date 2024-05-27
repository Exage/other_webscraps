import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By

link = "https://by.kari.com/by/muzhchinam/aksessuary/sumki-i-ryukzaki/"

@pytest.fixture(scope="function")
def browser():
    browser = webdriver.Chrome()
    yield browser
    browser.quit()

def test_page_title(browser):
    browser.get(link)
    elem = browser.find_element(By.CSS_SELECTOR, "div.page_title h1")
    assert elem.text == "СУМКИ И РЮКЗАКИ", "Нет"

@pytest.mark.parametrize('page', [f'https://by.kari.com/by/muzhchinam/aksessuary/sumki-i-ryukzaki/?PAGEN_1={i}' for i in range(1, 6)])
def test_multiple_pages(browser, page):
    browser.get(page)
    elems = browser.find_elements(By.CSS_SELECTOR, "a.gtmProductClick")
    assert len(elems) > 0, f"На странице отсутсвют товары [{page}]"
