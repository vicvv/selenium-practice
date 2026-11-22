SELENIUM WITH PYTHON - MODULE 5: PAGE OBJECT MODEL


GOAL

Stop repeating locators and steps in every test. A page object is a Python class that represents one page of the app. It holds that page's locators and the actions a user can do there. Tests call those actions and check the results. Tests never contain locators.


THE PROBLEM PAGE OBJECTS SOLVE

In Module 4, the login steps and locators lived in the test file. With 3 tests that is fine. With 50 tests, if a developer renames the username field id, you fix it in 50 places, and you will probably miss a few.

With page objects, the locator lives in one place. You fix one line and every test works again.

Tests also become easier to read. Compare:

```python
driver.find_element(By.ID, "username").send_keys("tomsmith")
driver.find_element(By.ID, "password").send_keys("SuperSecretPassword!")
driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
```

with:

```python
LoginPage(driver).open().login_as("tomsmith", "SuperSecretPassword!")
```

The second one reads like the user's steps.


THE THREE PARTS

- tests/conftest.py - provides the browser (the driver fixture from Module 4)
- src/selenium_practice/pages/mod5_pages.py - page objects: locators and actions, no asserts
- tests/mod5_login_test.py - tests: call actions, assert results, no locators

The rule to remember: page objects know HOW to do things. Tests know WHAT should be true.


A PAGE OBJECT, STEP BY STEP

```python
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
        self.type_text(self.USERNAME, username)
        self.type_text(self.PASSWORD, password)
        self.click(self.SUBMIT)
```

- The locators are class attributes. They are the same tuples you used with waits in Module 2.
- Each method is something a user does on that page: open it, log in.
- The waits live inside the page object, so tests never need to think about them.
- open() returns self, so you can chain: LoginPage(driver).open().login(...)


BASE PAGE: SHARED HELPERS

Every page needs the same small helpers: wait for an element, click it, type into it. Instead of copying them into each page class, they live once in BasePage:

```python
class BasePage:
    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def find_visible(self, locator):
        return self.wait.until(EC.visibility_of_element_located(locator))

    def click(self, locator):
        self.wait.until(EC.element_to_be_clickable(locator)).click()
```

class LoginPage(BasePage) means LoginPage inherits from BasePage: it gets all of BasePage's helpers for free.

The helpers use the Module 2 rules: visibility before reading, clickable before clicking.


METHODS THAT RETURN THE NEXT PAGE

When an action takes the user to a different page, the method returns a page object for that new page:

```python
    def login_as(self, username, password):
        self.login(username, password)
        self.wait.until(EC.url_contains("/secure"))
        return SecureAreaPage(self.driver)
```

So the test always holds the right page object for where the user actually is:

```python
secure = LoginPage(driver).open().login_as(VALID_USER, VALID_PASSWORD)
login_page = secure.logout()
```

login() (no return) is for cases where the user stays on the login page, for example a failed login.


USING PAGE OBJECTS IN A TEST

```python
from selenium_practice.pages.mod5_pages import LoginPage

def test_wrong_password_shows_error(driver):
    login_page = LoginPage(driver).open()
    login_page.login(VALID_USER, "wrong-password")
    assert "Your password is invalid!" in login_page.flash_text()
    assert login_page.flash_is_error()
```

No By, no find_element, no waits in the test. Only steps and asserts.


WHERE THE PAGE OBJECTS LIVE: THE SELENIUM_PRACTICE PACKAGE

The page objects are not next to the tests. They live in a real Python package:

```
src/
    selenium_practice/          the package
        __init__.py
        pages/
            __init__.py
            mod5_pages.py       BasePage, LoginPage, SecureAreaPage
            mod6_pages.py       Module 6 page objects
```

- Each __init__.py marks its folder as a Python package. They can be almost empty.
- pyproject.toml in the repo root describes the package, so pip can install it.
- The import path follows the folders: selenium_practice.pages.mod5_pages means src/selenium_practice/pages/mod5_pages.py.

The package is installed in editable mode, from the repo root, with the venv active:

```
pip install -e .
```

pip install -r requirements.txt does the same, because its last line is -e .

- The dot means "the package in this folder".
- -e (editable) means Python reads the files straight from src/. A change to a page object takes effect on the next run, with no reinstall.
- The install creates a src/selenium_practice.egg-info/ folder. It is in .gitignore and must never be committed.

Check that it is installed:

```
python -c "import selenium_practice.pages.mod5_pages; print('import OK')"
```

Why a package, instead of keeping the page objects next to the tests:

- The import works the same way whichever folder you run pytest from, because Python finds the installed package, not a file that happens to sit in the current folder.
- Other code can reuse the page objects. mod6_pages.py imports BasePage from here, and another project could install the package straight from GitHub.
- Tests and reusable code are clearly separated: tests/ only holds tests.

Why the file names still use underscores: a dash in a module name breaks the import. Python reads the dash as a minus sign:

```python
from selenium_practice.pages.mod5-pages import LoginPage   # SyntaxError
from selenium_practice.pages.mod5_pages import LoginPage   # works
```

The same is true for the package itself: the project is called selenium-practice, with a dash, but the import name is selenium_practice, with an underscore.

VS Code: if the import line is underlined in yellow, VS Code is using a different Python. Press Cmd+Shift+P, choose "Python: Select Interpreter", and pick the one in venv. This only affects VS Code's suggestions, not how the tests run.


WHY IT MATTERS / TRAPS (READ THIS PART!)

Trap 1 - Asserts inside page objects.
A page object that asserts decides what "correct" means, so every test that uses it is stuck with that decision. Page objects return values (flash_text(), url, is_loaded()). Tests assert on them. Exception: waiting for a page to be ready inside a page object is fine, because that is "how", not "what should be true".

Trap 2 - Locators leaking into tests.
One driver.find_element(By.ID, ...) in a test file brings the old problem back: a renamed field now breaks a test that the page object fix will not repair. If a test needs something new from a page, add a method to the page object.

Trap 3 - A dash in an imported name.
"from selenium_practice.pages.mod5-pages import LoginPage" fails with a SyntaxError. Any file or folder that is imported must have no dashes in its name.

Trap 4 - Reading the old page after navigation.
Right after clicking Logout, the old page's flash banner can still be found for a moment, so you would read "You logged into a secure area!" instead of "You logged out of the secure area!". The fix: the page object waits for the URL to change (EC.url_contains) before returning the next page. Same lesson as the Module 3 checkboxes: wait for the result before you read it. Doing it inside the page object means no test ever has to remember.

Trap 5 - time.sleep() inside a page object.
A sleep hidden in a page method slows down every test that calls it, and it is still flaky. Use the wait helpers.

Trap 6 - One giant page class.
One class for the whole app becomes impossible to maintain. Use one class per page. A part shared by many pages (like a top menu) can be its own class.

Trap 7 - Running a test file with python3.
python3 tests/mod5_login_test.py does nothing useful: the file only defines functions, and nothing provides the driver fixture. Test files always run through pytest.

Trap 8 - The package is not installed.
Every test that imports a page object fails with "ModuleNotFoundError: No module named 'selenium_practice'". Usual causes: the venv is not active, a new venv was created, or a fresh clone skipped the install. Activate the venv and run pip install -e . (or pip install -r requirements.txt).


READING A PAGE OBJECT FAILURE

When a locator is wrong, the error is usually a TimeoutException, and the traceback goes through two files:

- The line in tests/mod5_login_test.py tells you which test and which step failed.
- The line in src/selenium_practice/pages/mod5_pages.py tells you which method and which locator timed out.

Read the traceback from the bottom up: the last lines show where it actually broke.


HANDS-ON PRACTICE

Files:

- tests/conftest.py - the driver fixture
- src/selenium_practice/pages/mod5_pages.py - BasePage, LoginPage, SecureAreaPage
- tests/mod5_login_test.py - four tests: valid login, wrong password, unknown username, logout

1. Check the package is installed:

```
python -c "import selenium_practice.pages.mod5_pages; print('import OK')"
```

2. Run only the Module 5 tests:

```
python3 -m pytest tests/mod5_login_test.py -v
```

   Expect 4 passed.

3. Run everything:

```
python3 -m pytest -v
```

Break it on purpose (this step is MEANT to fail):

1. In src/selenium_practice/pages/mod5_pages.py, line 52, change
   USERNAME = (By.ID, "username")
   to
   USERNAME = (By.ID, "user-name")
   To confirm the line number: grep -n "USERNAME = " src/selenium_practice/pages/mod5_pages.py
2. Run the Module 5 tests. All 4 fail with TimeoutException, about 10 seconds each, because every test goes through LoginPage.open().
3. Look at the traceback: it points to open() in src/selenium_practice/pages/mod5_pages.py. Because the package is installed in editable mode, your change took effect without reinstalling.
4. Change line 52 back. One edit, and all 4 pass again.

That is the whole point of page objects: many tests break, but there is only one place to fix.


MENTAL MODEL

- Before: locators copied into every test.
  Now: locators in one page class.
- Before: tests full of find_element, click and send_keys.
  Now: tests read like the user's steps.
- Before: a renamed field means many fixes.
  Now: a renamed field means one fix.
- Page objects live in the selenium_practice package, tests live in tests/.
- Page objects: how to do things. Tests: what should be true.


FOR YOUR OWN APP LATER

- Start with a login page object. Almost every other test needs it.
- One class per screen.
- If the app uses custom dropdowns (built from div elements, not select), hide the "click to open, then click the option" steps inside one method, like choose_status("In Use"). Tests stay simple even when the UI is complicated.


QUIZ (answers below - try before peeking)

1. A developer renames the password field id. You have 30 tests that log in. With page objects, how many places do you change, and in which file?

2. Where does this line belong, in a page object or in a test, and why?
   assert "Welcome" in flash.text

3. Why does "from selenium_practice.pages.mod5-pages import LoginPage" fail?

4. Why does logout() wait for the URL to contain "/login" before returning a LoginPage? What could go wrong without it?

5. What does login_as() return, and why is returning the next page useful?

6. You find driver.find_element(By.ID, "username") in a test file. What is wrong, and how do you fix it?

7. After cloning the repo on a new Mac and creating a venv, every Module 5 test fails with "No module named 'selenium_practice'". What did you forget?

8. DevOps stretch question: a developer's pull request renames the username field. How could your team find out BEFORE the change is merged, not after? (Covered in Module 10. Just guess.)


ANSWERS

1. One place: the PASSWORD locator in src/selenium_practice/pages/mod5_pages.py. Every test uses LoginPage, so all 30 are fixed at once.

2. In a test. Page objects say how to do things. Tests decide what should be true. The page object should provide flash_text(), and the test asserts on it.

3. Python reads the dash as a minus sign, so it is a syntax error. Anything that is imported must have no dashes in its name (mod5_pages, selenium_practice).

4. Right after the click, the old page can still be on screen for a moment. Without the wait, flash_text() could read the old banner ("You logged into a secure area!") and the test would fail, or worse, pass for the wrong reason. Waiting for the URL change makes sure you read the new page.

5. A SecureAreaPage object. The test then holds the object for the page the user is actually on, so it can only call actions that exist on that page (like logout()).

6. A locator has leaked into the test. If the field is renamed, the page object fix will not repair this test. Add a method to LoginPage for whatever the test needs, and call that method instead.

7. Installing the package. The venv is new, so it does not contain selenium_practice yet. With the venv active, run pip install -r requirements.txt, which installs the pinned packages and, because of its -e . line, the package too.

8. Run the Selenium tests automatically in CI (for example GitHub Actions) on every pull request. The tests fail, the pull request shows a red check, and with branch protection requiring that check to pass, it cannot be merged until the page object locator is updated too, usually in the same pull request.


End of Module 5. Next up: Module 6, tricky elements (alerts, iframes, multiple tabs and windows, file uploads).