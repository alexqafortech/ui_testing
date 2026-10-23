import pytest
from playwright.sync_api import expect

@pytest.mark.catalog
def test_catalog_product_count(page):
    page.goto("/catalog")

    expect(page.locator("#products-grid > div")).to_have_count(5)

@pytest.mark.catalog
def test_each_card_has_title_and_price(page):
    page.goto("/catalog")
    cards = page.locator("#products-grid > div")
    count = cards.count()

    for i in range(count):
        card = cards.nth(i)
        expect(card.locator("h3")).to_be_visible()
        expect(card.locator("div[class='p-4']>p")).to_be_visible()

@pytest.mark.catalog
def test_add_specific_product_to_cart(page):
    page.goto("/catalog")
    card = page.locator("#products-grid > div").filter(has_text="iPhone 15")
    page.on("dialog", lambda dialog: dialog.accept())
    card.get_by_role("button", name="В корзину").click()
    expect(page.locator("a[href='/cart']>span")).to_be_visible()
    expect(page.locator("a[href='/cart']>span")).not_to_have_text("0")

@pytest.mark.catalog
def test_strict_mod_demo(page):
    page.goto("/catalog")
    try:
        page.get_by_role("button", name="В корзину").click()
    except Exception as e:
        print(e)

    page.get_by_role("button", name="В корзину").first.click()
    # Strict mode в Playwright - это изюминка Playwright, она не дает нам делать неоднозначные действия, из-за чего появляется
    #необходимость уточнять, какую именно кнопку нажать, в отличие от Selenium. find_element в Selenium молча брал первый
    #попавшийся элемент и проводил с ним операцию. По моему мнению это особенность "палка о двух концах", в некоторых
    #моментах было удобно добавить просто первый элемент, но в целом, strict mode увеличивает стабильность тестов.


