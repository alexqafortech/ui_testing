import pytest
from playwright.sync_api import expect

@pytest.mark.auth
def test_profile_without_login(authenticated_page):
    page = authenticated_page
    page.goto("/profile")
    expect(page.locator("#profile-content")).to_be_visible()

@pytest.mark.auth
def test_orders_without_login(authenticated_page):
    page = authenticated_page
    page.goto("/orders")
    page.wait_for_load_state("networkidle")
    expect(page).to_have_url("/orders")