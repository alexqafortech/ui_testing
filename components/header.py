from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time

from pages.base_page import BasePage

class HeaderComponent(BasePage):
    LOGO_LOCATOR = (By.XPATH, "//a[contains(text(),'ШопМаркет')]")
    CATALOG_LOCATOR = (By.CSS_SELECTOR, "a[href='/catalog']")
    CART_LOCATOR = (By.CSS_SELECTOR, "a[href='/cart']")
    CART_COUNT_LOCATOR = (By.CSS_SELECTOR, "a[href='/cart'] > span")
    MENU_TRIGGER_LOCATOR = (By.CSS_SELECTOR, "div[class='relative group']")
    PROFILE_LOCATOR = (By.CSS_SELECTOR, "a[href='/profile']")
    LOGOUT_LOCATOR = (By.CSS_SELECTOR, "button[onclick='logout()']")

    def get_cart_count(self) -> int:
        time.sleep(0.15)
        try:
            counter_element = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located(self.CART_COUNT_LOCATOR)
            )
            text_value = counter_element.get_attribute("textContent").strip()
            if not text_value:
                return 0
            return int(text_value)
        except (TimeoutException, ValueError):
            return 0

    def go_to_catalog(self):
        self.click(self.CATALOG_LOCATOR)

    def go_to_cart(self):
        self.click(self.CART_LOCATOR)

    def open_user_menu(self):
        trigger = self.find(self.MENU_TRIGGER_LOCATOR)
        ActionChains(self.driver).move_to_element(trigger).perform()

    def go_to_profile(self):
        self.open_user_menu()
        self.click(self.PROFILE_LOCATOR)

    def logout(self):
        self.open_user_menu()
        self.click(self.LOGOUT_LOCATOR)

