class PlaywrightBasePage:

    def __init__(self, page, base_url: str="http://82.146.39.180:3000"):
        self.page = page
        self.base_url = base_url

    def navigate(self, path=""):
        self.page.goto(self.base_url + path)
        return self

    def get_title(self):
        return self.page.title()

    def current_url(self):
        return self.page.url

    def screenshot(self, path):
        self.page.screenshot(path=path)
