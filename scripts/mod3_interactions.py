"""
mod3_interactions.py
Selenium Module 3 — Browser Interactions practice
(login flow, dropdown, checkboxes)

Run with the venv activated:
    source venv/bin/activate
    python3 FILES/interactions.py
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()

# ---------- PART A: LOGIN FLOW ----------
driver.get("https://the-internet.herokuapp.com/login")

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
driver.get("https://the-internet.herokuapp.com/dropdown")

dropdown = Select(
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "dropdown"))
    )
)
dropdown.select_by_visible_text("Option 2")
print("Selected:", dropdown.first_selected_option.text)

# ---------- PART C: CHECKBOXES (robust + wait for state) ----------
driver.get("https://the-internet.herokuapp.com/checkboxes")

boxes = driver.find_elements(By.CSS_SELECTOR, "#checkboxes input")

for i, box in enumerate(boxes):
    if not box.is_selected():
        box.click()
    # Wait until THIS checkbox is actually selected before moving on
    WebDriverWait(driver, 5).until(lambda d, b=box: b.is_selected())
    print(f"Checkbox {i+1} selected?", box.is_selected())

time.sleep(3) 

driver.quit()