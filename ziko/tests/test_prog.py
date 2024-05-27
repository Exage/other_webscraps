import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By

link = "https://ziko.by/catalog/naruchnye-chasy"

@pytest.fixture(scope="function")
def browser():
    browser = webdriver.Chrome()
    yield browser
    browser.quit()

def test_watch_count(browser):
    browser.get(link)
    time.sleep(10)
    watches = browser.find_elements(By.CSS_SELECTOR, "div.product")
    assert len(watches) > 0, "На странице нет часов"

def test_watch_prices(browser):
    browser.get(link)
    time.sleep(10)
    prices = browser.find_elements(By.CSS_SELECTOR, "a.price")
    assert len(prices) > 0, "На странице нет цен часов"
    for price in prices:
        assert price.text.replace('\t', '').replace('\n', '').split(' руб.')[0], "Found an empty watch title"

@pytest.mark.parametrize('page', [f'https://ziko.by/catalog/naruchnye-chasy?page={i}' for i in range(1, 6)])
def test_multiple_pages(browser, page):
    browser.get(page)
    watches = browser.find_elements(By.CSS_SELECTOR, "div.product")
    assert len(watches) == 40, f"Не найдено нужного кол-ва часов на странице {page}"
