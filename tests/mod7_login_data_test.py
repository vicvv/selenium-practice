"""
mod7_login_data_test.py
Selenium Module 7: data-driven tests with pytest parametrize.
One test function runs once per case. Each case gets its own browser.

Uses LoginPage from the selenium_practice package
(src/selenium_practice/pages/mod5_pages.py) and test data from
mod7_login_cases.csv, which sits in the same folder as this file (tests/).

Run from the repo root with the venv active:
    python3 -m pytest tests/mod7_login_data_test.py -v
"""

import csv
from pathlib import Path

import pytest

from selenium_practice.pages.mod5_pages import LoginPage

DATA_FILE = Path(__file__).parent / "mod7_login_cases.csv"


def load_login_cases():
    """Read the CSV file and turn each row into one test case."""
    with open(DATA_FILE, newline="") as f:
        return [
            pytest.param(row["username"], row["password"], row["expected"], id=row["case"])
            for row in csv.DictReader(f)
        ]


# ---------- CASES WRITTEN IN THE CODE ----------

@pytest.mark.parametrize(
    "username, password, expected",
    [
        pytest.param("tomsmith", "supersecretpassword!", "Your password is invalid!", id="lowercase-password"),
        pytest.param("tom", "SuperSecretPassword!", "Your username is invalid!", id="partial-username"),
        pytest.param("", "", "Your username is invalid!", id="both-empty"),
    ],
)
def test_failed_login_inline(driver, username, password, expected):
    login_page = LoginPage(driver).open()
    login_page.login(username, password)
    assert expected in login_page.flash_text()
    assert login_page.flash_is_error()


# ---------- CASES LOADED FROM THE CSV FILE ----------

@pytest.mark.parametrize("username, password, expected", load_login_cases())
def test_failed_login_from_csv(driver, username, password, expected):
    login_page = LoginPage(driver).open()
    login_page.login(username, password)
    assert expected in login_page.flash_text()
    assert login_page.flash_is_error()