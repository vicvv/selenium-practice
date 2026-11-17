"""
mod9_debug_test.py
Selenium Module 9: logging, screenshots and page source.

Run from the repo root with the venv active:
    python3 -m pytest FILES/mod9_debug_test.py -v --log-cli-level=INFO
"""

import logging

from mod5_pages import LoginPage

logger = logging.getLogger(__name__)

VALID_USER = "tomsmith"
VALID_PASSWORD = "SuperSecretPassword!"   # public demo login, not a real secret


def test_login_with_logged_steps(driver):
    logger.info("Opening the login page")
    login_page = LoginPage(driver).open()

    logger.info("Logging in as %s", VALID_USER)   # never log the password
    secure = login_page.login_as(VALID_USER, VALID_PASSWORD)

    logger.info("Checking the secure area")
    assert secure.is_loaded()
    assert "You logged into a secure area!" in secure.flash_text()


def test_screenshot_can_be_saved(driver, tmp_path):
    LoginPage(driver).open()
    shot = tmp_path / "mod9_login.png"
    assert driver.save_screenshot(str(shot)), "save_screenshot returned False"
    assert shot.exists()
    assert shot.stat().st_size > 0


def test_page_source_contains_login_form(driver):
    LoginPage(driver).open()
    assert 'id="username"' in driver.page_source