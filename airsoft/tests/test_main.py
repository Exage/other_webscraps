import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By

link = "https://airsoft-rus.ru/catalog/1020/"

@pytest.fixture(scope="function")
def browser():
    browser = webdriver.Chrome()
    yield browser
    browser.quit()

def test_logo(browser):
    browser.get(link)
    logo = browser.find_element(By.CSS_SELECTOR, "span.logo a").text
    assert logo == "AirSoft-RUS", "Ошибка в логотипе"

def test_title(browser):
    browser.get(link)
    title = browser.find_element(By.CSS_SELECTOR, "#content h1").text
    assert title == "Оружие для страйкбола", "Ошибка в заголовке!"

@pytest.mark.parametrize('page', [f'https://airsoft-rus.ru/catalog/1020/?PAGEN_1={i}' for i in range(1, 6)])
def test_count_products(browser, page):
    browser.get(page)
    products = browser.find_elements(By.CSS_SELECTOR, "div.item")
    assert len(products) == 24, f"Не найдено нужного количества товаров на странице {page}"




