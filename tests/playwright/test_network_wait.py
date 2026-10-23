import pytest
from playwright.sync_api import expect
from pages.playwright.login_page import PlaywrightLoginPage
from pages.playwright.catalog_page import PlaywrightCatalogPage

@pytest.mark.network
def test_add_to_cart_sends_request(parallel_page, parallel_user_registered):
    page = parallel_page
    user = parallel_user_registered

    page.on("dialog", lambda alert: alert.accept())

    login = PlaywrightLoginPage(page)
    login.open()
    login.login(user["email"], user["password"])

    expect(login.get_username()).to_have_text(user["username"])

    catalog = PlaywrightCatalogPage(page)
    catalog.open()
    page.wait_for_load_state("networkidle")

    counter = page.locator("a[href='/cart']>span")
    initial_count = int(counter.text_content())


    with page.expect_response("**/api/cart**") as resp:
        catalog.add_product_by_name("iPhone 15")

    assert resp.value.status == 200
    assert resp.value.json()

    expect(counter).to_have_text(str(initial_count + 1))

@pytest.mark.network
def test_add_to_cart_request_body(parallel_page, parallel_user_registered):
    page = parallel_page
    user = parallel_user_registered

    page.on("dialog", lambda alert: alert.accept())

    login = PlaywrightLoginPage(page)
    login.open()
    login.login(user["email"], user["password"])
    expect(login.get_username()).to_have_text(user["username"])

    catalog = PlaywrightCatalogPage(page)
    catalog.open()
    page.wait_for_load_state("networkidle")

    with page.expect_request(
            lambda request: "api/cart" in request.url and request.method == "POST"
    ) as req_info:
        catalog.add_product_by_name("iPhone 15")

    request = req_info.value
    req_body = request.post_data_json

    assert req_body
    assert "productId" in req_body

    assert req_body["productId"]

@pytest.mark.network
def test_add_to_cart_full(parallel_page, parallel_user_registered):
    page = parallel_page
    user = parallel_user_registered

    page.on("dialog", lambda alert: alert.accept())

    login = PlaywrightLoginPage(page)
    login.open()
    login.login(user["email"], user["password"])

    expect(login.get_username()).to_have_text(user["username"])

    catalog = PlaywrightCatalogPage(page)
    catalog.open()
    page.wait_for_load_state("networkidle")

    counter = page.locator("a[href='/cart']>span")
    initial_count = int(counter.text_content()) if counter.is_visible() else 0

    with page.expect_response("**/api/cart**") as resp:
        page.get_by_role("button", name="В корзину").first.click()

    assert resp.value.status in (200, 201)
    expect(counter).to_have_text(str(initial_count + 1))

