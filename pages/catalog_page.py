from pages.base_page import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import json

class CatalogPage(BasePage):

    PRODUCT_CARD = (By.CSS_SELECTOR, "#products-grid > div")
    ADD_TO_CART_BTN = (By.XPATH, ".//button[contains(text(), 'В корзину')]")
    CART_COUNTER = (By.CSS_SELECTOR, "a[href='/cart'] > span")
    IPHONE_ITEM = (By.CSS_SELECTOR, "a[href='/product/1']")
    FIRST_CARD = (By.CSS_SELECTOR, "#products-grid > div:first-child > a")
    PATH = "/catalog"

    def open(self):
        return super().open(self.PATH)

    def get_products(self):
        return WebDriverWait(self.driver, 10).until(
            lambda d: d.find_elements(*self.PRODUCT_CARD)
            if len(d.find_elements(*self.PRODUCT_CARD)) >= 5
            else False
        )

    def get_cart_count(self) -> int:
        elements = self.driver.find_elements(*self.CART_COUNTER)

        if not elements:
            return 0

        count = elements[0].text.strip()
        return int(count) if count else 0

    def add_first_product_to_cart(self):
        self.click(self.ADD_TO_CART_BTN)

    def add_product_to_cart(self, index: int):
        products = self.get_products()
        products[index].find_element(*self.ADD_TO_CART_BTN).click()

    def wait_for_cart_count(self, expected_count: int):
        self.wait_until(
            lambda _: self.get_cart_count() == expected_count
        )

    def get_localstorage_cart_count(self) -> int:
        data = self.driver.execute_script(
            "return localStorage.getItem('cart_items')"
        )

        if not data or data == "null":
            return 0

        return len(json.loads(data))

    def clear_localstorage_cart(self):
        self.driver.execute_script(
            "localStorage.removeItem('cart_items')"
        )