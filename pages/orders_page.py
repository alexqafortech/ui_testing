from pages.base_page import BasePage
from selenium.webdriver.common.by import By


class OrdersPage(BasePage):
    PATH = "/orders"
    ORDER_ROW = (By.CSS_SELECTOR, "div[id='orders-content'] a")
    ORDER_STATUS = (By.CSS_SELECTOR, "div[class='text-right'] span")

    def open(self):
        return super().open(self.PATH)

    def get_order_count(self) -> int:
        return len(self.find_all(self.ORDER_ROW))

    def get_latest_order_status(self):
        item = self.find_all(self.ORDER_ROW)
        first = item[0]
        return first.find_element(*self.ORDER_STATUS).text