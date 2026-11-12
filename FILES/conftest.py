"""
conftest.py
Shared pytest fixtures for all modules.
pytest loads this file automatically, so tests never import it.
Keep this exact file name - pytest will not find it otherwise.
"""

import pytest
from selenium import webdriver


@pytest.fixture
def driver():
    drv = webdriver.Chrome()   # SETUP: fresh browser for each test
    yield drv                  # the test runs here
    drv.quit()                 # TEARDOWN: always runs, pass or fail