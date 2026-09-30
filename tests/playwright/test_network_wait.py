import pytest
from playwright.sync_api import expect

# Проблема этих тестов состоит в том, что без авторизации не отправляются запросы /api/cart, которые нам нужны для
# проверки, вместо них получаем запрос me со статусом 401.
# Если же мы будем делать с авторизацией, то наткнемся на проблему, что количество товаров в корзине растёт, из-за
# этого третий тест уже падает. Если мы будем сбрасывать БД, то не сможем воспользоваться общей сессией, потому что
# вместе с очисткой БД, у нас будет удаляться и id сессии, в связи с чем тесты начнут падать уже со второго. Очистка
# localstorage могла бы сработать, в случае, если бы мы не авторизировались, но так как нам необходимо авторизация,
# нам нужно "сбрасывать" БД

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

    # Пользователь авторизован -> данные хранятся не в localStorage, а в БД
    #page.wait_for_function("localStorage.getItem('cart_items') !== null")
    #localstorage = page.evaluate("localStorage.getItem('cart_items')")
    #assert localstorage is not None

