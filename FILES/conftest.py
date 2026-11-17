"""
conftest.py
Shared pytest fixtures, options and hooks for all modules.
pytest loads this file automatically, so tests never import it.
Keep this exact file name - pytest will not find it otherwise.

Options:
    python3 -m pytest FILES/ -v               # with a window (default)
    python3 -m pytest FILES/ -v --headless    # without a window

When a test fails, a screenshot and the page HTML are saved in
the screenshots/ folder in the repo root (that folder is in .gitignore).
"""

import logging
import re
from datetime import datetime
from pathlib import Path

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

WINDOW_SIZE = "1280,800"
SCREENSHOT_DIR = Path(__file__).resolve().parent.parent / "screenshots"

logger = logging.getLogger(__name__)


def pytest_addoption(parser):
    parser.addoption(
        "--headless",
        action="store_true",
        default=False,
        help="Run Chrome without a visible window",
    )


@pytest.hookimpl(wrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    """Store each phase's result on the test (rep_setup, rep_call,
    rep_teardown), so fixtures can check whether the test failed."""
    report = yield
    setattr(item, f"rep_{report.when}", report)
    return report


def build_chrome_options(headless, accept_insecure_certs=False):
    """Build the settings Chrome starts with."""
    opts = Options()
    if headless:
        opts.add_argument("--headless=new")
    opts.add_argument(f"--window-size={WINDOW_SIZE}")   # always, see Module 8 Trap 1
    opts.accept_insecure_certs = accept_insecure_certs
    return opts


def save_failure_evidence(request, drv):
    """If the test failed, save a screenshot and the page HTML."""
    report = getattr(request.node, "rep_call", None)
    if report is None or not report.failed:
        return
    try:
        SCREENSHOT_DIR.mkdir(exist_ok=True)
        safe_name = re.sub(r"[^A-Za-z0-9_-]", "_", request.node.name)
        stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        png_file = SCREENSHOT_DIR / f"{safe_name}_{stamp}.png"
        html_file = SCREENSHOT_DIR / f"{safe_name}_{stamp}.html"
        drv.save_screenshot(str(png_file))
        html_file.write_text(drv.page_source, encoding="utf-8")
        logger.warning("Saved failure screenshot: %s", png_file)
    except Exception as exc:
        logger.warning("Could not save failure evidence: %s", exc)


def start_browser(request, accept_insecure_certs=False):
    headless = request.config.getoption("--headless")
    logger.info("Starting Chrome (headless=%s)", headless)
    return webdriver.Chrome(
        options=build_chrome_options(headless, accept_insecure_certs)
    )


@pytest.fixture
def driver(request):
    """A fresh browser for each test. Certificate errors are NOT ignored."""
    drv = start_browser(request)
    yield drv                                # the test runs here
    try:
        save_failure_evidence(request, drv)  # only does something if the test failed
    finally:
        drv.quit()                           # always runs


@pytest.fixture
def insecure_driver(request):
    """A fresh browser that ignores certificate errors.
    Only for trusted dev or test sites."""
    drv = start_browser(request, accept_insecure_certs=True)
    yield drv
    try:
        save_failure_evidence(request, drv)
    finally:
        drv.quit()