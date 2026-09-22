import pytest
from selenium.webdriver.common.by import By
import time

CATALOG_URL = "/catalog"

@pytest.mark.catalog
def test_catalog_displays_five_products(browser, base_url):
    browser.get(base_url + CATALOG_URL)
    time.sleep(2) # TODO: заменить на explicit wait в практике 3
    product_items = browser.find_elements(By.CSS_SELECTOR, "#products-grid > div")
    assert len(product_items) == 5

@pytest.mark.catalog
def test_each_product_card_has_title_and_price(browser, base_url):
    browser.get(base_url + CATALOG_URL)
    time.sleep(2) # TODO: заменить на explicit wait в практике 3
    product_items = browser.find_elements(By.CSS_SELECTOR, "#products-grid > div")
    assert len(product_items) == 5
    for card in product_items:
        card.find_element(By.CSS_SELECTOR, "h3")
        name_of_card = card.text.split("\n")[0]
        price = card.text.split("\n")[2]
        assert name_of_card is not None
        assert price is not None

@pytest.mark.catalog
def test_iphone_product_is_in_catalog(browser, base_url):
    browser.get(base_url + CATALOG_URL)
    time.sleep(2) # TODO: заменить на explicit wait в практике 3
    iphone_item = browser.find_element(By.XPATH, "//h3[.='iPhone 15 Pro 256GB']")
    assert iphone_item.is_displayed()

@pytest.mark.catalog
def test_clicking_product_card_opens_product_page(browser, base_url):
    browser.get(base_url + CATALOG_URL)
    time.sleep(2) # TODO: заменить на explicit wait в практике 3

    first_item = browser.find_element(By.CSS_SELECTOR, "#products-grid > div:first-child > a")
    first_item.click()
    time.sleep(2) # TODO: заменить на explicit wait в практике 3

    assert browser.current_url == f"{base_url}/product/1"