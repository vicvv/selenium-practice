from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

driver = webdriver.Chrome()
driver.get("https://www.selenium.dev/selenium/web/web-form.html")

# 1. By NAME (a text input named "my-text")
text_box = driver.find_element(By.NAME, "my-text")
text_box.send_keys("hello locators")

# 2. By CSS_SELECTOR (the password field)
pwd = driver.find_element(By.CSS_SELECTOR, "input[name='my-password']")
pwd.send_keys("secret123")

# 3. By find_elements (count all the input fields on the page)
inputs = driver.find_elements(By.TAG_NAME, "input")
print("Number of <input> elements found:", len(inputs))

# 4. Safe existence check using find_elements (no crash if missing)
maybe = driver.find_elements(By.ID, "does-not-exist")
print("Did we find the fake element?", len(maybe) > 0)   # prints False

# 5. By XPATH using visible text (the Submit button)
submit = driver.find_element(By.XPATH, "//button[text()='Submit']")

time.sleep(3)   # pause so you can SEE the filled form (debug only!)
submit.click()  # submits the form -> page changes

# After submit, read the confirmation message
msg = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "message"))
)
print("Confirmation text:", msg.text)

time.sleep(3)
driver.quit()