import pytest
from components.product_card import ProductCard

@pytest.mark.smoke
@pytest.mark.catalog
def test_catalog_displays_five_products(catalog_page):
    catalog_page.open()
    products = len(catalog_page.get_products())
    assert products >= 5

@pytest.mark.catalog
def test_each_product_card_has_title_and_price(catalog_page):
    catalog_page.open()

    product_items = catalog_page.get_products()

    for card in product_items:
        card_text = [
            line.strip()
            for line in card.text.splitlines()
            if line.strip()
        ]

    assert card_text[0]
    assert card_text[2]

@pytest.mark.catalog
def test_iphone_product_is_in_catalog(catalog_page):
    catalog_page.open()

    iphone_item = catalog_page.find(catalog_page.IPHONE_ITEM)
    assert iphone_item.is_displayed()

@pytest.mark.catalog
def test_clicking_product_card_opens_product_page(catalog_page):
    catalog_page.open()
    catalog_page.click(catalog_page.FIRST_CARD)
    catalog_page.wait_for_url_contains("/product/1")

@pytest.mark.catalog
def test_each_product_card_complete(catalog_page):
    catalog_page.open()

    cards = catalog_page.get_products()

    for card_item in cards:
        card = ProductCard(card_item)
        assert card.get_title() != ""
        assert card.get_price() != ""
