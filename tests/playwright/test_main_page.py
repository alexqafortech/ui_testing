import pytest

@pytest.mark.smoke
def test_main_page_has_correct_title(page):
    page.goto("/")
    assert "ШопМаркет" in page.title()

@pytest.mark.smoke
def test_main_page_hero_banner(page):
    page.goto("/")
    assert page.inner_text("h1") != ""

@pytest.mark.smoke
def test_cta_button_leads_to_catalog(page):
    page.goto("/")
    page.click("a[href='/catalog']")
    assert "/catalog" in page.url

