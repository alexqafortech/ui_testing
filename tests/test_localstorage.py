import pytest
import json
from selenium.webdriver.common.by import By
from helpers.custom_conditions import cart_count_equals
from selenium.webdriver.support.ui import WebDriverWait
from helpers.waits import wait_for_element, wait_for_clickable
from selenium.webdriver.support import expected_conditions as EC

CATALOG_URL = "/catalog"

@pytest.mark.javascript
def test_cart_stored_in_localstorage(browser, base_url):
    browser.get(base_url+CATALOG_URL)

    wait_for_element(browser, (By.CSS_SELECTOR, "div[id='products-grid'] > div"))

    start_data = browser.execute_script("return localStorage.getItem('cart_items')")

    if start_data and start_data != "null":
        start_data_json = json.loads(start_data)
        start_data_length = len(start_data_json)
    else:
        start_data_length = 0

    cart_locator = (By.CSS_SELECTOR, "a[href='/cart'] > span")

    try:
        counter = browser.find_element(*cart_locator)
        counter_text = counter.get_attribute("textContent").strip()
        counter_value = int(counter_text) if counter_text else 0
    except Exception:
        counter_value = 0

    old_counter_value = counter_value

    wait_for_clickable(browser, (By.XPATH, "//button[contains(text(), 'В корзину')]")).click()
    WebDriverWait(browser, 10).until(EC.alert_is_present())
    alert = browser.switch_to.alert
    alert.accept()

    WebDriverWait(browser, 10).until(cart_count_equals(old_counter_value + 1, cart_locator))

    final_counter_text = browser.find_element(*cart_locator).get_attribute("textContent").strip()
    final_counter_value = int(final_counter_text) if final_counter_text else 0
    assert final_counter_value == old_counter_value + 1

    final_data = browser.execute_script("return localStorage.getItem('cart_items')")
    final_data_json = json.loads(final_data)
    final_data_length = len(final_data_json)

    assert final_data_length == start_data_length + 1

@pytest.mark.javascript
def test_clear_localstorage_empties_cart(browser, base_url):
    browser.get(base_url+CATALOG_URL)

    wait_for_element(browser, (By.CSS_SELECTOR, "div[id='products-grid'] > div"))

    cart_locator = (By.CSS_SELECTOR, "a[href='/cart'] > span")

    try:
        counter = browser.find_element(*cart_locator)
        counter_text = counter.get_attribute("textContent").strip()
        counter_value = int(counter_text) if counter_text else 0
    except Exception:
        counter_value = 0

    old_counter_value = counter_value

    wait_for_clickable(browser, (By.XPATH, "//button[contains(text(), 'В корзину')]")).click()
    WebDriverWait(browser, 10).until(EC.alert_is_present())
    alert = browser.switch_to.alert
    alert.accept()

    WebDriverWait(browser, 10).until(cart_count_equals(old_counter_value + 1, cart_locator))

    final_counter_text = browser.find_element(*cart_locator).get_attribute("textContent").strip()
    final_counter_value = int(final_counter_text) if final_counter_text else 0
    assert final_counter_value == old_counter_value + 1

    browser.execute_script("localStorage.removeItem('cart_items')")

    browser.refresh()

    wait_for_element(browser, (By.CSS_SELECTOR, "div[id='products-grid'] > div"))

    WebDriverWait(browser, 10).until(cart_count_equals(0, cart_locator))

    final_counter_text = browser.find_element(*cart_locator).get_attribute("textContent").strip()
    final_counter_value = int(final_counter_text) if final_counter_text else 0

    assert final_counter_value == 0
