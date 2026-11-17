"""
mod8_settings_test.py
Selenium Module 8: window size, certificate errors, and credentials
read from environment variables.

Run from the repo root with the venv active:
    python3 -m pytest FILES/mod8_settings_test.py -v -rs
    python3 -m pytest FILES/mod8_settings_test.py -v --headless

The login test needs these set in the terminal first:
    export TEST_USER=tomsmith
    export TEST_PASSWORD='SuperSecretPassword!'
"""

import os

import pytest

from mod5_pages import LoginPage

# badssl.com is a public site made for testing certificate errors
BAD_CERT_URL = "https://self-signed.badssl.com/"


def get_credentials():
    """Read the login from environment variables, or skip the test."""
    user = os.environ.get("TEST_USER")
    password = os.environ.get("TEST_PASSWORD")
    if not user or not password:
        pytest.skip("Set TEST_USER and TEST_PASSWORD to run this test")
    return user, password


def test_window_size_is_set(driver):
    size = driver.get_window_size()
    assert size["width"] == 1280, f"Expected width 1280, got {size['width']}"


def test_bad_certificate_blocked_by_default(driver):
    driver.get(BAD_CERT_URL)
    assert "Privacy error" in driver.title


def test_bad_certificate_accepted_when_allowed(insecure_driver):
    insecure_driver.get(BAD_CERT_URL)
    assert "Privacy error" not in insecure_driver.title
    assert "badssl" in insecure_driver.title


def test_login_with_env_credentials(driver):
    user, password = get_credentials()
    secure = LoginPage(driver).open().login_as(user, password)
    assert secure.is_loaded()