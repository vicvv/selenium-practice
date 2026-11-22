SELENIUM WITH PYTHON - MODULE 4: ASSERTIONS AND PYTEST


GOAL

Turn scripts that print results into real tests that pass or fail on their own.
Instead of reading print() output and deciding by eye, the test checks the result
itself (an assertion). pytest runs all the tests and reports PASSED or FAILED
for each one.


ONE-TIME SETUP (venv active)

```
cd ~/Documents/selenium-practice
source venv/bin/activate
pip install pytest
pip freeze > requirements.txt
echo ".pytest_cache/" >> .gitignore
```

pytest creates a .pytest_cache/ folder when it runs. It is junk, like venv/,
so we keep it out of Git.


ASSERTIONS - THE CORE IDEA

An assertion is a statement that must be true. If it is true, nothing happens.
If it is false, the test fails right there.

```python
assert driver.title == "Login Page"
assert "secure area" in flash.text
assert checkbox.is_selected()
assert len(rows) == 3
assert "/secure" not in driver.current_url
```

Add a message so a failure explains itself:

```python
assert "/secure" in driver.current_url, f"Expected /secure, got {driver.current_url}"
```

Before and after:

- print("Selected?", box.is_selected())   becomes   assert box.is_selected()
- print("Title:", driver.title)           becomes   assert driver.title == "Login Page"
- print("Message:", msg.text)             becomes   assert "Received!" in msg.text


HOW PYTEST FINDS YOUR TESTS

pytest finds tests by name. Nothing is registered by hand.

- The file name must start with test_ (or end with _test.py).
  test_login.py is found. login.py is ignored.
- The function name must start with test_.
  def test_valid_login() is found. def check_login() is ignored.

Run from the repo root:

```
python3 -m pytest tests/ -v                  # all tests in tests/, verbose
python3 -m pytest tests/test_basics.py -v    # one file
python3 -m pytest tests/ -v -k login         # only tests with "login" in the name
python3 -m pytest tests/ -v -s               # -s shows print() output
```


FIXTURES - SETUP AND TEARDOWN DONE RIGHT

Every test needs a browser and must close it afterwards, even if the test fails.
A pytest fixture handles that.

Put this in tests/conftest.py. pytest loads this file automatically,
so you never import it.

```python
import pytest
from selenium import webdriver

@pytest.fixture
def driver():
    drv = webdriver.Chrome()   # SETUP: runs before each test
    yield drv                  # the test runs here
    drv.quit()                 # TEARDOWN: always runs, pass or fail
```

A test asks for the fixture just by naming it as a parameter:

```python
def test_something(driver):    # pytest sees "driver" and calls the fixture
    driver.get("https://example.com")
```

Each test gets its own fresh browser, so tests do not affect each other.


WHY IT MATTERS / TRAPS (read this part!)

Trap 1 - The always-true assert.
assert (x == 5, "x should be 5") with parentheses NEVER fails. You have written
a tuple, and a non-empty tuple always counts as True. Python even warns about it.
Correct: assert x == 5, "x should be 5"  (no parentheses around both parts).

Trap 2 - Wrong names mean silently skipped tests.
A file called login_tests.py or a function called check_login() is ignored.
pytest reports "0 tests" or skips it without any error, so you think you are
covered when nothing ran. If the count of tests looks low, check the names.

Trap 3 - Exact match vs. contains.
The success banner text on the-internet also contains a newline and the close
button character at the end. So
assert flash.text == "You logged into a secure area!"  FAILS.
Use "in" for messages:
assert "You logged into a secure area!" in flash.text
Save == for values you fully control.

Trap 4 - Asserting before waiting.
Asserting on .text right after a click can read the page before it has updated
(the Module 3 checkbox lesson again). Wait for the right condition first,
then assert.

Trap 5 - driver.quit() at the end of the test body.
If an assertion fails first, that line never runs and Chrome windows pile up.
The fixture code after yield ALWAYS runs. Never put the quit inside the test.

Trap 6 - Tests that depend on each other.
"test_2 assumes test_1 already logged in" breaks as soon as tests run in a
different order, alone, or in parallel. Every test must set up everything it
needs. That is why each test calls login() itself.

Trap 7 - pytest vs python3 -m pytest.
Plain "pytest" can pick up a pytest installed somewhere else on your Mac
(outside the venv), which then cannot find Selenium.
"python3 -m pytest" always uses the venv Python.
If you see ModuleNotFoundError: selenium under pytest, this is why.

Trap 8 - Where did my prints go?
pytest hides print() output from passing tests. Use -s to see it.
Better still, use assertions and you will not need prints.


READING PYTEST OUTPUT

A passing run:

```
tests/test_basics.py::test_valid_login_shows_success PASSED
tests/test_basics.py::test_wrong_password_shows_error PASSED
tests/test_basics.py::test_all_checkboxes_can_be_checked PASSED
=========== 3 passed ===========
```

When a test fails, pytest shows which assert failed, the actual value, and the
expected value. Read the lines starting with E first. They tell you exactly
what went wrong.

```
>       assert "Welcome!" in flash.text
E       AssertionError: assert 'Welcome!' in 'You logged into a secure area!...'
```


HANDS-ON PRACTICE

Files (both in tests/):

- conftest.py - the driver fixture
- test_basics.py - three real tests: valid login, wrong password, checkboxes

Run:

```
python3 -m pytest tests/ -v
```

Three Chrome windows open and close one after another, because each test gets
a fresh browser. That is expected.

Break it on purpose (do this, it is the most useful part):
in test_valid_login_shows_success, change the expected text to "Welcome!",
run again, and read the failure output. Then change it back.
Seeing a failure helps you trust the passes.


MENTAL MODEL

- Before: driver = webdriver.Chrome() at the top of the script.
  Now: a driver fixture in conftest.py.
- Before: print(...) and read it yourself.
  Now: assert ... and pytest decides.
- Before: driver.quit() at the bottom.
  Now: after yield in the fixture, always runs.
- Before: one long script.
  Now: many small, independent test_ functions.
- Before: "looks right to me".
  Now: "3 passed" or "1 failed".


QUIZ (answers below - try before peeking)

1. You named a file login_checks.py with a function test_login(). You run
   python3 -m pytest tests/ and get "0 items collected". Why?

2. What does this do, and why is it dangerous?
   assert (len(rows) == 3, "expected 3 rows")

3. Why put driver.quit() after yield in a fixture instead of at the end of
   each test?

4. A teammate's assert flash.text == "You logged into a secure area!" fails even
   though login clearly worked. What is the likely cause and the fix?

5. test_search only passes when run after test_login. What is wrong with the
   design?

6. pytest says ModuleNotFoundError: No module named 'selenium', but your scripts
   run fine with python3. What is the quickest fix?

7. DevOps stretch question: you push these tests to GitHub Actions. The runner
   is a Linux machine with no screen. Which line in conftest.py will cause
   problems, and what do you think the fix is called? (Covered in Module 8.
   Just guess.)


ANSWERS

1. The FILE name does not start with test_ (and does not end with _test.py),
   so pytest never opens it, even though the function name is right.
   Rename it to test_login_checks.py.

2. It is a tuple, which always counts as True, so it can never fail.
   The check is silently disabled.
   Write: assert len(rows) == 3, "expected 3 rows"

3. If an assertion fails, the rest of the test does not run, so a quit() at the
   end gets skipped and browsers pile up. The fixture code after yield always
   runs, pass or fail.

4. The banner text also contains a newline and the close button character,
   so == does not match exactly.
   Use: "You logged into a secure area!" in flash.text

5. The tests depend on each other. Each test must set up its own state
   (log in itself, for example) so it passes alone, in any order, or in
   parallel.

6. Run python3 -m pytest with the venv active, so pytest uses the venv Python,
   where Selenium is installed. Plain "pytest" was probably a different install.

7. webdriver.Chrome() tries to open a visible browser window, and there is no
   screen to show it on. The fix is headless mode (Chrome runs without a
   visible window), set through Chrome options. That is Module 8, and it is
   also the link to your CI/CD learning.


End of Module 4. Next up: Module 5, Page Object Model (stop repeating locators
in every test, and organize tests so they stay maintainable as they grow).