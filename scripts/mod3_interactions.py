"""
mod3_interactions.py
Selenium Module 3 - Browser Interactions practice
(login flow, dropdown, checkboxes)

Run from the repo root with the venv active:
    python3 scripts/mod3_interactions.py
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

BASE = "https://the-internet.herokuapp.com"
CHECKBOXES = (By.CSS_SELECTOR, "#checkboxes input")

# Turn off Chrome's password manager and leaked-password warning.
# The demo password is public, so Chrome flags it as leaked, and the
# warning pop-up covers the page and can swallow clicks.
opts = Options()
opts.add_experimental_option("prefs", {
    "credentials_enable_service": False,
    "profile.password_manager_enabled": False,
    "profile.password_manager_leak_detection": False,
})

driver = webdriver.Chrome(options=opts)
try:
    # ---------- PART A: LOGIN FLOW ----------
    driver.get(f"{BASE}/login")

    user = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "username"))
    )
    user.clear()
    user.send_keys("tomsmith")

    pwd = driver.find_element(By.ID, "password")
    pwd.send_keys("SuperSecretPassword!")
    pwd.send_keys(Keys.RETURN)

    flash = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "flash"))
    )
    print("Login result:", flash.text.split("\n")[0])

    # ---------- PART B: DROPDOWN ----------
    driver.get(f"{BASE}/dropdown")

    dropdown = Select(
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "dropdown"))
        )
    )
    dropdown.select_by_visible_text("Option 2")
    print("Selected:", dropdown.first_selected_option.text)

    # ---------- PART C: CHECKBOXES (wait for each step) ----------
    driver.get(f"{BASE}/checkboxes")

    # Wait until the checkboxes are on the page, then count them
    WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located(CHECKBOXES))
    count = len(driver.find_elements(*CHECKBOXES))

    for i in range(1, count + 1):
        # A locator for checkbox number i, found fresh each time
        box_locator = (By.CSS_SELECTOR, f"#checkboxes input:nth-of-type({i})")

        # 1. Wait until it can be clicked
        box = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(box_locator))

        # 2. Click only if it is not ticked yet
        if not box.is_selected():
            box.click()

        # 3. Wait until it really reports ticked
        WebDriverWait(driver, 10).until(EC.element_located_to_be_selected(box_locator))
        print(f"Checkbox {i} selected?", driver.find_element(*box_locator).is_selected())

finally:
    driver.quit()   # always close the browser, even if a step above fails