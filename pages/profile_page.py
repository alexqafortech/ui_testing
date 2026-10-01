from selenium.webdriver.common.by import By
from components.header import HeaderComponent
from pages.base_page import BasePage


class ProfilePage(BasePage):

    PROFILE_CONTENT = (By.ID, "profile-content")
    PATH = "/profile"

    def __init__(self, driver, base_url = None):
        super().__init__(driver, base_url) if base_url else super().__init__(driver)
        self.header = HeaderComponent(driver)

    def open(self):
        return super().open(self.PATH)

    def is_loaded(self) -> bool:
        return self.is_visible(self.PROFILE_CONTENT)