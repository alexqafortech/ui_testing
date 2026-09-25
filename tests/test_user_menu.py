import pytest


@pytest.mark.navigation
def test_user_menu_navigate_to_profile(login_page, main_page, profile_page, create_user_with_hard_password):
    login_page.open()

    login_page.login("test_hard_pass@test.com", "HardPassword123!")

    main_page.open_user_profile()
    main_page.wait_for_url_contains("/profile")

    assert profile_page.is_loaded()

