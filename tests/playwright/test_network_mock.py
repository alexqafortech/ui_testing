import pytest
import json
from playwright.sync_api import expect

@pytest.mark.network
def test_catalog_renders_mocked_products(page):
    mock_products = [
        {
            "id": 15,
            "name": "Product 1",
            "category": "Электроника",
            "price": "15000.00",
            "description": "Product-1\", color: cool",
            "image_url": "/images/products/iphone-15-pro.svg"
        },
        {
            "id": 16,
            "name": "Product 2",
            "category": "Электроника",
            "price": "20000.00",
            "description": "Product-2\", memory: 128 GB",
            "image_url": "/images/products/iphone-15-pro.svg"
        },
    ]
    def handler(route):
        route.fulfill(
            status=200,
            content_type="application/json",
            body=json.dumps(mock_products)
        )
    page.route("/api/products", handler)

    with page.expect_response("/api/products") as response_info:
        page.goto("/catalog")

    assert response_info.value.status == 200
    expect(page.locator("#products-grid > div")).to_have_count(2)

@pytest.mark.network
def test_empty_catalog_mock(page):
    mock_products = []
    def handler(route):
        route.fulfill(
            status=200,
            content_type="application/json",
            body=json.dumps(mock_products)
        )
    page.route("/api/products", handler)

    with page.expect_response("/api/products") as response_info:
        page.goto("/catalog")

    assert response_info.value.status == 200
    expect(page.locator("#products-grid > div")).to_have_count(0)
    # При пустом каталоге, сайт ничего не показывает, на месте, где должны быть товары пустое место
    #expect(page.get_by_text("не")).to_be_visible()

@pytest.mark.network
def test_catalog_network_error(page):
    page.route("/api/products", lambda route: route.abort())

    page.goto("/catalog")
    expect(page.get_by_text("Загрузка")).to_be_visible()
    # Поведение проекта пахнет багов уровня Critical, в случае, если обрывается соединение, пользователю отображается
    # сообщение "Загружается", когда по факту ничего не загружается, потому что запрос сеть отвалилась

