from components.playwright.header import PlaywrightHeader
from pages.playwright.base_page import PlaywrightBasePage
from pages.playwright.orders_page import PlaywrightOrdersPage

PATH = "/cart"

class PlaywrightCartPage(PlaywrightBasePage):
    def __init__(self, page, base_url = None):
        super().__init__(page)
        self.header = PlaywrightHeader(page)
        self.cart_item = page.locator("#cart-content > div:first-child")
        self.promo_input = page.get_by_role("textbox", name="Введите промокод")
        self.promo_button = page.get_by_role("button", name="Применить")
        self.total = page.locator("div[id='cart-content'] > div:last-child > div > div:last-child > span:last-child")
        self.discount = page.locator("div[id='cart-content'] > div:last-child > div:nth-child(3) > div:nth-child(2) > span:nth-child(2)")
        self.checkout_button = page.get_by_role("button", name="Оформить заказ")

    def open(self):
        self.navigate(PATH)
        return self

    def get_cart_item(self):
        return self.cart_item

    def apply_promo(self, code: str):
        self.promo_input.fill(code)
        self.promo_button.click()

    def get_total(self):
        return self.total

    def get_discount(self):
        return self.discount

    def checkout(self):
        dialog_step = 1

        def handle_dialog(dialog):
            nonlocal dialog_step
            if dialog_step == 1:
                dialog.accept("Дмитрий Иванов")
            elif dialog_step == 2:
                dialog.accept("88005553535")
            elif dialog_step == 3:
                dialog.accept("улица Пушкина, д.1")
            elif dialog_step == 4:
                dialog.accept()
            dialog_step += 1

        self.page.on("dialog", handle_dialog)
        self.checkout_button.click()
        self.page.remove_listener("dialog", handle_dialog)
        self.page.wait_for_load_state("networkidle")
        return PlaywrightOrdersPage(self.page)