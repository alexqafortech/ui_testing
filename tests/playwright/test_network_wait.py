import pytest
from playwright.sync_api import expect

@pytest.mark.network
def test_add_to_cart_sends_request(authenticated_page):
    # Без авторизации api/cart не отправляется
    page = authenticated_page
    page.on("dialog", lambda alert: alert.accept())
    page.goto("/catalog")
    page.wait_for_load_state("networkidle")
    counter = page.locator("a[href='/cart']>span")
    initial_count = int(counter.text_content()) if counter.is_visible() else 0

    with page.expect_response("api/cart") as resp:
        page.get_by_role("button", name="В корзину").first.click()

    assert resp.value.status == 200
    assert resp.value.json

    expect(counter).to_have_text(str(initial_count + 1))

@pytest.mark.network
def test_add_to_cart_request_body(authenticated_page):
    page = authenticated_page
    page.on("dialog", lambda alert: alert.accept())
    page.goto("/catalog")
    item = page.get_by_role("button", name="В корзину").first

    with (page.expect_request(lambda request: "api/cart" in request.url and request.method == "POST")
          as req_info):
        item.click()

    request = req_info.value

    req_body = request.post_data_json
    assert req_body

    assert "productId" in req_body
    assert str(req_body["productId"]) == "1"

@pytest.mark.network
def test_add_to_cart_full(authenticated_page):
    page = authenticated_page
    page.on("dialog", lambda alert: alert.accept())
    page.goto("/catalog")
    page.wait_for_load_state("networkidle")
    counter = page.locator("a[href='/cart']>span")
    initial_count = int(counter.text_content()) if counter.is_visible() else 0

    with page.expect_response("api/cart") as resp:
        page.get_by_role("button", name="В корзину").first.click()

    assert resp.value.status == 200

    expect(counter).to_have_text(str(initial_count + 1))


