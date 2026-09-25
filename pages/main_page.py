from pages.base_page import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

class MainPage(BasePage):
    HERO_TITLE = (By.CSS_SELECTOR, "a[href='/']")
    CTA_BUTTON = (By.PARTIAL_LINK_TEXT, "Каталог")
    PRODUCTS_CARDS = (By.CSS_SELECTOR, "div[id = 'featured-products']> div")
    PARTIAL = By.PARTIAL_LINK_TEXT
    USER_MENU = (By.CSS_SELECTOR, "div[class='relative group']")
    PROFILE_LINK = (By.CSS_SELECTOR, "a[href='/profile']")
    PATH = "/"

    def open(self):
        return super().open(self.PATH)

    def get_hero_title(self) -> str:
        return self.get_text(self.HERO_TITLE)

    def click_cta(self):
        self.click(self.CTA_BUTTON)

    def get_product_count(self) -> int:
        return len(self.find_all(self.PRODUCTS_CARDS))

    def open_user_profile(self):
        user_menu = self.find(self.USER_MENU)

        ActionChains(self.driver).move_to_element(user_menu).perform()

        self.click(self.PROFILE_LINK)

