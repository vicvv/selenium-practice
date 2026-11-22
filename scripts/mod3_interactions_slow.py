"""
mod3_interactions_slow.py
Selenium Module 3 - the same practice as mod3_interactions.py, SLOWED DOWN
with time.sleep() pauses so you can watch each step.
The pauses are for watching only - never use time.sleep() to wait in real tests.

Run from the repo root with the venv active:
    python3 scripts/mod3_interactions_slow.py
"""

import time

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
    time.sleep(1)                       # watch the username get typed

    pwd = driver.find_element(By.ID, "password")
    pwd.send_keys("SuperSecretPassword!")
    time.sleep(1)                       # watch the password get typed

    pwd.send_keys(Keys.RETURN)

    flash = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "flash"))
    )
    print("Login result:", flash.text.split("\n")[0])
    time.sleep(2)                       # watch the success banner

    # ---------- PART B: DROPDOWN ----------
    driver.get(f"{BASE}/dropdown")

    dropdown = Select(
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "dropdown"))
        )
    )
    dropdown.select_by_visible_text("Option 2")
    print("Selected:", dropdown.first_selected_option.text)
    time.sleep(2)                       # watch the dropdown selection

    # ---------- PART C: CHECKBOXES (wait for each step) ----------
    driver.get(f"{BASE}/checkboxes")

    WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located(CHECKBOXES))
    count = len(driver.find_elements(*CHECKBOXES))

    for i in range(1, count + 1):
        box_locator = (By.CSS_SELECTOR, f"#checkboxes input:nth-of-type({i})")

        box = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(box_locator))
        if not box.is_selected():
            box.click()

        WebDriverWait(driver, 10).until(EC.element_located_to_be_selected(box_locator))
        print(f"Checkbox {i} selected?", driver.find_element(*box_locator).is_selected())
        time.sleep(1)                   # watch each checkbox get ticked

    time.sleep(3)                       # final pause before closing

finally:
    driver.quit()   # always close the browser, even if a step above fails