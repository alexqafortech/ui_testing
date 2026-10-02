from components.playwright.header import PlaywrightHeader
from pages.playwright.base_page import PlaywrightBasePage


class PlaywrightCatalogPage(PlaywrightBasePage):

    PATH = "/catalog"

    def __init__(self, page, base_url= None):
        super().__init__(page)

        self.header = PlaywrightHeader(page)
        self.cards = page.locator("#products-grid")
        self.product = page.locator("#products-grid > div")

    def open(self):
        self.navigate(self.PATH)
        return self

    def add_product_by_name(self, name):
        card = self.product.filter(has_text=name)
        card.get_by_role("button", name="В корзину").click()

