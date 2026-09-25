from pages.base_page import BasePage
from selenium.webdriver.common.by import By

class AdminPage(BasePage):

    PATH = "/admin"
    USERS_TABLE = (By.CSS_SELECTOR, "#users-table > div > table > tbody > tr")
    ITEM = (By.XPATH, "//td[contains(., 'test_user')]/following-sibling::td[1]")
    BLOCK_USER = (By.XPATH, "//td[contains(text(), 'ivanov_d')]/following-sibling::td[5]/div/button[contains(text(), 'Заблокировать')]")
    ACTIVATE_USER = (By.XPATH, "//td[contains(text(), 'test_hard_pass')]/following-sibling::td[5]/div/button[contains(text(), 'Активировать')]")
    TEXT_BLOCK_LOCATOR = (By.XPATH, "//td[contains(text(), 'ivanov_d')]/following-sibling::td[3]")
    RELOAD_LOCATOR = (By.ID, "reset-db-btn")

    def open(self):
        return super().open(self.PATH)

    def reload_page(self):
        self.driver.refresh()

    def reload_data_base(self):
        self.click(self.RELOAD_LOCATOR)
        self.alert_accept()

    def activate_user(self):
        self.click(self.ACTIVATE_USER)