from components.playwright.header import PlaywrightHeader
from pages.playwright.base_page import PlaywrightBasePage

PATH = "/orders"

class PlaywrightOrdersPage(PlaywrightBasePage):

    def __init__(self, page, base_url = None):
        super().__init__(page)
        self.header = PlaywrightHeader(page)
        self.order_rows = page.locator("#orders-content>div>a")


    def open(self):
        self.navigate(PATH)

    def get_orders(self):
        return self.order_rows

