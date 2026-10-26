"""
interactions.py
Selenium Module 3 — Browser Interactions practice
(SLOWED DOWN so you can watch each step)
"""

import time
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
driver.get("https://the-internet.herokuapp.com/dropdown")

dropdown = Select(
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "dropdown"))
    )
)
dropdown.select_by_visible_text("Option 2")
print("Selected:", dropdown.first_selected_option.text)
time.sleep(2)                       # watch the dropdown selection

# ---------- PART C: CHECKBOXES (robust + wait for state) ----------
driver.get("https://the-internet.herokuapp.com/checkboxes")

boxes = driver.find_elements(By.CSS_SELECTOR, "#checkboxes input")
for i, box in enumerate(boxes):
    if not box.is_selected():
        box.click()
    WebDriverWait(driver, 5).until(lambda d, b=box: b.is_selected())
    print(f"Checkbox {i+1} selected?", box.is_selected())
    time.sleep(1)                   # watch each checkbox get ticked

time.sleep(3)                       # final pause before closing
driver.quit()