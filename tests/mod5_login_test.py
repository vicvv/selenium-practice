"""
mod5_login_test.py
Selenium Module 5: tests that use page objects.
No locators in this file - they all live in mod5_pages.py.

Run from the repo root with the venv active:
    python3 -m pytest tests/mod5_login_test.py -v
"""

from selenium_practice.pages.mod5_pages import LoginPage

VALID_USER = "tomsmith"
VALID_PASSWORD = "SuperSecretPassword!"


def test_valid_login_reaches_secure_area(driver):
    secure = LoginPage(driver).open().login_as(VALID_USER, VALID_PASSWORD)
    assert secure.is_loaded()
    assert "You logged into a secure area!" in secure.flash_text()


def test_wrong_password_shows_error(driver):
    login_page = LoginPage(driver).open()
    login_page.login(VALID_USER, "wrong-password")
    assert "Your password is invalid!" in login_page.flash_text()
    assert login_page.flash_is_error()


def test_unknown_username_shows_error(driver):
    login_page = LoginPage(driver).open()
    login_page.login("nobody", VALID_PASSWORD)
    assert "Your username is invalid!" in login_page.flash_text()
    assert login_page.flash_is_error()


def test_logout_returns_to_login_page(driver):
    secure = LoginPage(driver).open().login_as(VALID_USER, VALID_PASSWORD)
    login_page = secure.logout()
    assert "You logged out of the secure area!" in login_page.flash_text()
    assert "/login" in login_page.url