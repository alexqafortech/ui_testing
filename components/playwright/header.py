class PlaywrightHeader:
    def __init__(self, page):
        self.page=page
        self.logo = page.get_by_role("link", name="ШопМаркет")
        self.catalog = page.get_by_role("link", name="Каталог")
        self.cart = page.locator("a[href='/cart']")
        self.support = page.get_by_role("link", name="Поддержка")
        self.login = page.get_by_role("link", name="Войти")
        self.registration = page.get_by_role("link", name="Зарегистрироваться")
        self.user = page.locator("div[class='relative group']")
        self.cart_count = page.locator("a[href='/cart']>span")

    def get_cart_count(self):
        return self.cart_count

    def go_to_catalog(self):
        self.catalog.click()

    def go_to_cart(self):
        self.cart.click()


