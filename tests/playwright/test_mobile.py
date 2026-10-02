import pytest
from playwright.sync_api import Playwright, Browser, expect


@pytest.fixture
def mobile_context(browser, playwright, storage_state_path_api):
    iphone = playwright.devices["iPhone 13"]
    context = browser.new_context(**iphone, storage_state=storage_state_path_api)
    yield context
    context.close()

def test_mobile_version(mobile_context, base_url):
    page = mobile_context.new_page()
    page.goto(base_url)
    expect(page.get_by_role("heading", name="Весенняя распродажа")).to_be_visible(timeout=5000)
    expect(page.get_by_text("© 2026 ШопМаркет. Учебный проект.")).to_be_visible()
