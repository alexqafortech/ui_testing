from selenium.webdriver.common.by import By

class ProductCard:
    TITLE = (By.CSS_SELECTOR, "div[class='p-4'] h3")
    PRICE = (By.CSS_SELECTOR, "div[class='p-4'] > p")
    ADD_BTN = (By.CSS_SELECTOR, "div[class='p-4'] > button")

    def __init__(self, root_element):
        self.root = root_element

    def get_title(self):
        return self.root.find_element(*self.TITLE).text

    def get_price(self):
        return self.root.find_element(*self.PRICE).text

    def add_to_cart(self):
        self.root.find_element(*self.ADD_BTN).click()

