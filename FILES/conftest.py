"""
conftest.py
Shared pytest fixtures and options for all modules.
pytest loads this file automatically, so tests never import it.
Keep this exact file name - pytest will not find it otherwise.

Options:
    python3 -m pytest FILES/ -v               # with a window (default)
    python3 -m pytest FILES/ -v --headless    # without a window
"""

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

WINDOW_SIZE = "1280,800"


def pytest_addoption(parser):
    parser.addoption(
        "--headless",
        action="store_true",
        default=False,
        help="Run Chrome without a visible window",
    )


def build_chrome_options(headless, accept_insecure_certs=False):
    """Build the settings Chrome starts with."""
    opts = Options()
    if headless:
        opts.add_argument("--headless=new")
    opts.add_argument(f"--window-size={WINDOW_SIZE}")   # always, see Module 8 Trap 1
    opts.accept_insecure_certs = accept_insecure_certs
    return opts


@pytest.fixture
def driver(request):
    """A fresh browser for each test. Certificate errors are NOT ignored."""
    headless = request.config.getoption("--headless")
    drv = webdriver.Chrome(options=build_chrome_options(headless))
    yield drv                  # the test runs here
    drv.quit()                 # always runs, pass or fail


@pytest.fixture
def insecure_driver(request):
    """A fresh browser that ignores certificate errors.
    Only for trusted dev or test sites."""
    headless = request.config.getoption("--headless")
    drv = webdriver.Chrome(
        options=build_chrome_options(headless, accept_insecure_certs=True)
    )
    yield drv
    drv.quit()