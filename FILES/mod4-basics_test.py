"""
mod4-basics_test.py
Selenium Module 4: real PASS/FAIL tests with pytest.

Run from the repo root with the venv active:
    python3 -m pytest FILES/ -v
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

BASE = "https://the-internet.herokuapp.com"


def login(driver, username, password):
    """Helper: log in and return the flash message element."""
    driver.get(f"{BASE}/login")
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "username"))
    ).send_keys(username)
    driver.find_element(By.ID, "password").send_keys(password)
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    return WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "flash"))
    )


def test_valid_login_shows_success(driver):
    flash = login(driver, "tomsmith", "SuperSecretPassword!")
    assert "You logged into a secure area!" in flash.text
    assert "success" in flash.get_attribute("class")
    assert "/secure" in driver.current_url, f"Expected /secure, got {driver.current_url}"


def test_wrong_password_shows_error(driver):
    flash = login(driver, "tomsmith", "wrong-password")
    assert "Your password is invalid!" in flash.text
    assert "error" in flash.get_attribute("class")
    assert "/secure" not in driver.current_url


def test_all_checkboxes_can_be_checked(driver):
    driver.get(f"{BASE}/checkboxes")
    boxes = driver.find_elements(By.CSS_SELECTOR, "#checkboxes input")
    assert len(boxes) == 2, f"Expected 2 checkboxes, found {len(boxes)}"

    for box in boxes:
        if not box.is_selected():
            box.click()
        WebDriverWait(driver, 5).until(lambda d, b=box: b.is_selected())

    for i, box in enumerate(boxes, start=1):
        assert box.is_selected(), f"Checkbox {i} is not selected"