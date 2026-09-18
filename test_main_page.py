import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.expected_conditions import element_to_be_clickable
from selenium.webdriver.support.wait import WebDriverWait


@pytest.mark.smoke
@pytest.mark.main_page
def test_main_page_has_correct_title(browser, base_url):
    """Главная страница BuggyShop загружается с корректным заголовком."""
    browser.get(base_url)
    assert "ШопМаркет" in browser.title

@pytest.mark.main_page
def test_main_page_has_hero_heading(browser, base_url):
    """На главной странице отображается заголовок hero-баннера."""
    browser.get(base_url)
    heading = browser.find_element(By.TAG_NAME, "h1")
    assert heading.is_displayed()
    assert heading.text.strip() != ""

@pytest.mark.main_page
def test_cta_button_leads_to_catalog(browser, base_url):
    """Клик по ссылке 'Каталог' в шапке ведёт на страницу каталога."""
    browser.get(base_url)
    cta_button = WebDriverWait(browser, 10).until(element_to_be_clickable((By.PARTIAL_LINK_TEXT, "Каталог")))
    cta_button.click()

    assert "/catalog" in browser.current_url

@pytest.mark.parametrize("url_text, expected_url", [
    pytest.param("Каталог", "/catalog", id = "catalog_link"),
    pytest.param("Войти", "/login", id = "login_link"),
    pytest.param("Зарегистрироваться", "/register", id = "register_link"),
    pytest.param("ШопМаркет", "/", id = "main_link"),
    pytest.param("Поддержка", "/support", id = "support_link")
])
def test_header_link_leads_to_correct_page(browser, url_text, expected_url, base_url):
    browser.get(base_url)
    cta_button = WebDriverWait(browser, 10).until(element_to_be_clickable((By.PARTIAL_LINK_TEXT, url_text)))
    cta_button.click()

    assert expected_url in browser.current_url