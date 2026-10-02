import pytest
from playwright.sync_api import Playwright, expect
from pages.playwright.orders_page import PlaywrightOrdersPage
from pages.playwright.cart_page import PlaywrightCartPage

@pytest.mark.hybrid
def test_order_appears_in_ui(base_url, page, playwright_orders_page):
    api_context = page.context.request

    add_to_cart_response = api_context.post(
        f"{base_url}api/cart",
        data={
            "productId": 1
        }
    )
    assert add_to_cart_response.ok, f"Не удалось добавить товар в корзину: {add_to_cart_response.text}"

    checkout_response = api_context.post(
        f"{base_url}api/orders",
        data={
            "address": "ул. Пушкина 1",
            "customerName": "Name",
            "phone": "88005553535"
        }
    )
    assert checkout_response.ok, f"Не удалось оформить заказ через API: {checkout_response.text}"

    order_data = checkout_response.json()
    order_id = order_data.get("id") or order_data.get("orderId")
    assert order_id, "В ответе API отсутствует ID созданного заказа"

    orders = PlaywrightOrdersPage(page)
    orders.open()
    expect(orders.get_orders()).not_to_have_count(0)

@pytest.mark.hybrid
def test_prepared_cart_in_ui(base_url, page, playwright_cart_page):
    api_context = page.context.request

    add_to_cart_response = api_context.post(
        f"{base_url}api/cart",
        data={
            "productId": 1
        }
    )
    assert add_to_cart_response.ok, f"Не удалось наполнить корзину через API: {add_to_cart_response.text}"

    cart = PlaywrightCartPage(page)
    cart.open()
    expect(cart.get_cart_item()).not_to_have_count(0)