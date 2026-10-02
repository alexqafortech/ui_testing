from pages.playwright.base_page import PlaywrightBasePage

class PlaywrightLoginPage(PlaywrightBasePage):
    PATH = "/login"

    def __init__(self, page, base_url = None):
        super().__init__(page)

        self.email = page.get_by_role("textbox", name="email")
        self.password = page.get_by_role("textbox", name="Ваш пароль")
        self.submit = page.get_by_role("button", name="Войти")
        self.error = page.get_by_text("Неверный")
        self.block_error = page.get_by_text("Заблокирован")
        self.user_name = page.locator("div[class='relative group']>button")

    def open(self):
        self.navigate(self.PATH)
        return self

    def login(self, email: str | None, password: str | None):
        self.email.fill(email)
        self.password.fill(password)
        self.submit.click()
        return self

    def get_error(self):
        return self.error

    def get_username(self):
        return self.user_name

    def click_submit(self):
        self.submit.click()

    def get_email(self):
        return self.email
