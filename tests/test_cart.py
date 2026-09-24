import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from helpers.waits import wait_for_element, wait_for_clickable, wait_for_url_contains
from selenium.webdriver.support import expected_conditions as EC
from helpers.custom_conditions import cart_count_equals
import time

CATALOG_URL = "/catalog"
CART_URL = "/cart"

@pytest.mark.cart
def test_add_to_cart_increases_counter_lambda(browser, base_url):
    start = time.time()
    browser.get(base_url + CATALOG_URL)

    wait_for_element(browser, (By.CSS_SELECTOR, "div[id='products-grid'] > div"))

    try:
        counter = browser.find_element((By.CSS_SELECTOR, "a[href='/cart'] > span"))
        counter_text = counter.get_attribute("textContent").strip()
        counter_value = int(counter_text) if counter_text else 0
    except:
        counter_value = 0

    old_counter_value = counter_value

    wait_for_clickable(browser, (By.XPATH, "//button[contains(text(), 'В корзину')]")).click()
    WebDriverWait(browser, 10).until(EC.alert_is_present())
    alert = browser.switch_to.alert
    alert.accept()

    WebDriverWait(browser, 10).until(
        lambda b:
            int(b.find_element(By.CSS_SELECTOR, "a[href='/cart'] > span")
                .text.strip() or "0") == old_counter_value +1
    )

    final_counter_text = browser.find_element(By.CSS_SELECTOR, "a[href='/cart'] > span").text.strip()
    final_counter_value = int(final_counter_text) if final_counter_text else 0

    assert final_counter_value == old_counter_value+1
    duration = time.time() - start
    print(f"Логин занял {duration: .2f}s")

@pytest.mark.cart
def test_add_to_cart_increases_counter_factory(browser, base_url):
    start = time.time()
    browser.get(base_url + CATALOG_URL)

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
    duration = time.time() - start
    print(f"Логин занял {duration: .2f}s")

@pytest.mark.cart
def test_add_three_products_to_cart(browser, base_url):
    start = time.time()
    browser.get(base_url + CATALOG_URL)

    product_locator = (By.CSS_SELECTOR, "div[id='products-grid'] > div")
    carts = WebDriverWait(browser, 10).until(
        lambda b: b.find_elements(*product_locator) if len(b.find_elements(*product_locator)) >= 3
        else False
    )

    try:
        cart_element = browser.find_element(By.CSS_SELECTOR, "a[href='/cart'] > span")
        cart_text = cart_element.get_attribute("textContent").strip()
        start_cart_value = int(cart_text) if cart_text else 0
    except:
        start_cart_value = 0

    for i in range(3):
        expected_value = start_cart_value+i+1

        current_carts = browser.find_elements(*product_locator)
        target_product = current_carts[i]

        button = target_product.find_element(By.XPATH, ".//button[contains(text(), 'В корзину')]")
        button.click()

        WebDriverWait(browser, 10).until(EC.alert_is_present())
        browser.switch_to.alert.accept()

        WebDriverWait(browser, 10).until(
            lambda b: int(
                b.find_element(By.CSS_SELECTOR, "a[href='/cart'] > span")
                .get_attribute("textContent")
                .strip() or "0"
            ) == expected_value
        )
    final_text = browser.find_element(By.CSS_SELECTOR, "a[href='/cart'] > span").get_attribute("textContent").strip()
    final_value = int(final_text) if final_text else 0

    assert final_value == start_cart_value + 3, f"Ожидали в корзине {start_cart_value + 3}, но получили {final_value}"
    duration = time.time() - start
    print(f"Логин занял {duration: .2f}s")

@pytest.mark.cart
def test_cart_page_shows_added_products(browser, base_url):
    start = time.time()
    browser.get(base_url + CATALOG_URL)

    wait_for_element(browser, (By.CSS_SELECTOR, "div[id='products-grid'] > div"))

    try:
        counter = browser.find_element((By.CSS_SELECTOR, "a[href='/cart'] > span"))
        counter_text = counter.get_attribute("textContent").strip()
        counter_value = int(counter_text) if counter_text else 0
    except:
        counter_value = 0

    old_counter_value = counter_value

    wait_for_clickable(browser, (By.XPATH, "//button[contains(text(), 'В корзину')]")).click()
    WebDriverWait(browser, 10).until(EC.alert_is_present())
    alert = browser.switch_to.alert
    alert.accept()

    WebDriverWait(browser, 10).until(
        lambda b: int(
            b.find_element(By.CSS_SELECTOR, "a[href='/cart'] > span")
            .get_attribute("textContent")
            .strip() or "0"
        ) == old_counter_value + 1
    )

    try:
        wait_for_clickable(browser, (By.CSS_SELECTOR, "a[href='/cart']")).click()
    except:
        browser.find_element(By.CSS_SELECTOR, "a[href='/cart']").click()
    wait_for_url_contains(browser, "/cart")
    wait_for_element(browser, (By.CSS_SELECTOR, "div[id='cart-content']>div:first-child>div"))

    cart_products = browser.find_elements(By.CSS_SELECTOR, "div[id='cart-content']>div:first-child>div")

    assert len(cart_products) == 1
    duration = time.time() - start
    print(f"Логин занял {duration: .2f}s")
