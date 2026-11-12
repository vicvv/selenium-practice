from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()
driver.get("https://the-internet.herokuapp.com/dynamic_loading/1")

# 1. Click "Start" — wait until it's CLICKABLE first (good habit)
start_btn = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "#start button"))
)
start_btn.click()

# 2. A loading spinner appears, then after a few seconds the hidden
#    text "Hello World!" is revealed. Wait for it to be VISIBLE.
#    (If you tried to read it immediately, it would be empty/hidden.)
finish_text = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.ID, "finish"))
)

print("Revealed text:", finish_text.text)

# 3. Demonstrate a TIMEOUT on purpose.
#    We look for something that will never appear, with a short 3s
#    limit, and catch the error instead of crashing.
from selenium.common.exceptions import TimeoutException
try:
    WebDriverWait(driver, 3).until(
        EC.presence_of_element_located((By.ID, "this-will-never-exist"))
    )
except TimeoutException:
    print("As expected: timed out waiting for a missing element.")

driver.quit()