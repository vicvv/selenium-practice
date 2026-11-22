"""
mod10_smoke_test.py
Selenium Module 10: smoke tests - a small, quick check of the most
important features. The GitHub Actions workflow runs these first.

Run only the smoke tests, from the repo root with the venv active:
    python3 -m pytest -m smoke
"""

import pytest

from selenium_practice.pages.mod5_pages import LoginPage

VALID_USER = "tomsmith"
VALID_PASSWORD = "SuperSecretPassword!"   # public demo login, not a real secret


@pytest.mark.smoke
def test_smoke_login_page_loads(driver):
    login_page = LoginPage(driver).open()
    assert "/login" in login_page.url


@pytest.mark.smoke
def test_smoke_valid_login(driver):
    secure = LoginPage(driver).open().login_as(VALID_USER, VALID_PASSWORD)
    assert secure.is_loaded()