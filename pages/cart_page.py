from pages.base_page import BasePage
from selenium.webdriver.common.by import By
import json


class CartPage(BasePage):

    CART_PRODUCTS = (By.CSS_SELECTOR, "div[id='cart-content'] > div:first-child > div")
    CART_COUNTER = (By.CSS_SELECTOR, "a[href='/cart'] > span")
    PATH = "/cart"

    def open(self):
        return super().open(self.PATH)

    def get_cart_products(self):
        return self.find_all(self.CART_PRODUCTS)

    def get_cart_count(self) -> int:
        elements = self.driver.find_elements(*self.CART_COUNTER)

        if not elements:
            return 0

        count = elements[0].text.strip()
        return int(count) if count else 0

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

    def wait_for_cart_count(self, expected_count: int):
        self.wait_until(
            lambda _: self.get_cart_count() == expected_count
        )