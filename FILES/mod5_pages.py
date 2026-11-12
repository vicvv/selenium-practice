"""
mod5_pages.py
Selenium Module 5: page objects for the public practice site
the-internet.herokuapp.com.

Each class holds one page's locators and actions.
Tests import these classes. Tests never contain locators.
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

BASE_URL = "https://the-internet.herokuapp.com"


class BasePage:
    """Helpers shared by every page."""

    # This site shows the same flash banner on several pages
    FLASH = (By.ID, "flash")

    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def find_visible(self, locator):
        return self.wait.until(EC.visibility_of_element_located(locator))

    def click(self, locator):
        self.wait.until(EC.element_to_be_clickable(locator)).click()

    def type_text(self, locator, text):
        field = self.find_visible(locator)
        field.clear()
        field.send_keys(text)

    @property
    def url(self):
        return self.driver.current_url

    def flash_text(self):
        return self.find_visible(self.FLASH).text

    def flash_is_error(self):
        return "error" in self.find_visible(self.FLASH).get_attribute("class")


class LoginPage(BasePage):
    URL = f"{BASE_URL}/login"

    USERNAME = (By.ID, "username")
    PASSWORD = (By.ID, "password")
    SUBMIT = (By.CSS_SELECTOR, "button[type='submit']")

    def open(self):
        self.driver.get(self.URL)
        self.find_visible(self.USERNAME)   # page is ready when the field shows
        return self

    def login(self, username, password):
        """Fill in the form and submit. Use this when the login should fail."""
        self.type_text(self.USERNAME, username)
        self.type_text(self.PASSWORD, password)
        self.click(self.SUBMIT)

    def login_as(self, username, password):
        """Log in with valid credentials and return the page you land on."""
        self.login(username, password)
        self.wait.until(EC.url_contains("/secure"))
        return SecureAreaPage(self.driver)


class SecureAreaPage(BasePage):
    LOGOUT = (By.CSS_SELECTOR, "a[href='/logout']")

    def is_loaded(self):
        self.find_visible(self.LOGOUT)
        return "/secure" in self.url

    def logout(self):
        self.click(self.LOGOUT)
        self.wait.until(EC.url_contains("/login"))   # wait for the new page
        return LoginPage(self.driver)