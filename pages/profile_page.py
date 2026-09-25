from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class ProfilePage(BasePage):

    PROFILE_CONTENT = (By.ID, "profile-content")
    PATH = "/profile"

    def open(self):
        return super().open(self.PATH)

    def is_loaded(self) -> bool:
        return self.is_visible(self.PROFILE_CONTENT)