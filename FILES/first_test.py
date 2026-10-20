from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()            # launches Chrome
driver.get("https://www.google.com")   # open a page

# Wait up to 10 seconds for the search box to appear, then type in it
box = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.NAME, "q"))
)
box.send_keys("Selenium with Python")

print("Page title is:", driver.title)
input("Press Enter to close the browser...")
driver.quit()                          # close the browser cleanly
