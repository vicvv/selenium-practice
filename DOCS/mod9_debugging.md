SELENIUM WITH PYTHON - MODULE 9: DEBUGGING
(screenshots on failure, logging, HTML reports)


GOAL

Find out why a test failed, even when you could not watch it. Headless tests and tests on GitHub Actions have no window, so the evidence has to be saved. Three tools:

- Screenshots on failure: a picture of the page at the moment the test failed, plus the page's HTML.
- Logging: messages that say what the test was doing, step by step.
- An HTML report: all results in one page you open in a browser.


ONE-TIME SETUP (venv active)

Packages this course uses:

- selenium - drives the browser (setup, before Module 1)
- pytest - finds and runs the tests (Module 4)
- pytest-html - creates the HTML report (Module 9)

pip also installs the packages these depend on, so the install output lists more names than these three. That is normal.

Install them all at once. Packages that are already installed are skipped:

```
cd ~/Documents/selenium-practice
source venv/bin/activate
pip install selenium pytest pytest-html
pip freeze > requirements.txt
```

pip freeze writes every installed package and its version to requirements.txt, so the repo records exactly what the tests need. Run it again whenever you install something new.

Check what is installed:

```
pip list | grep -i -E "selenium|pytest"
```

Keep the evidence files out of Git:

```
echo "screenshots/" >> .gitignore
echo "report.html" >> .gitignore
echo "test-run.log" >> .gitignore
```

If a line was already in .gitignore, a duplicate is harmless.

On a new machine, or for anyone who clones the repo, create the venv and install everything from requirements.txt in one step:

```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Notes:

- pip only works with the venv active. Outside it, "pip" is usually not found on a Mac (setup notes).
- If pip prints "A new release of pip is available", that is only a notice. You can ignore it, or update pip with: pip install --upgrade pip


PART 1 - SCREENSHOTS ON FAILURE

Taking a screenshot by hand is one line:

```python
driver.save_screenshot("page.png")   # returns True if it worked
```

The useful part is doing it automatically, only when a test fails. Two pieces in conftest.py work together.

Piece 1 - a hook that records each test's result:

```python
@pytest.hookimpl(wrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    report = yield
    setattr(item, f"rep_{report.when}", report)
    return report
```

- pytest runs every test in three phases: setup (the fixture code before yield), call (the test itself) and teardown (the fixture code after yield).
- After each phase, pytest creates a report with the result. This hook runs around that step: yield lets pytest build the report, then the hook stores it on the test as rep_setup, rep_call or rep_teardown.
- You copy this hook as it is. It is a standard pattern from the pytest documentation.

Piece 2 - the fixture checks the result before closing the browser:

```python
@pytest.fixture
def driver(request):
    drv = webdriver.Chrome(options=build_chrome_options(headless))
    yield drv
    try:
        save_failure_evidence(request, drv)   # screenshot + HTML, only if the test failed
    finally:
        drv.quit()
```

- request.node is the current test. request.node.rep_call is the result of its call phase, stored by the hook.
- The call phase is finished before teardown starts, so when the fixture code after yield runs, the result is already known.
- save_failure_evidence() checks rep_call.failed. If the test passed, it does nothing.
- try/finally makes sure the browser is closed even if saving the screenshot goes wrong.

What gets saved, in a screenshots/ folder in the repo root:

- a .png picture of the page
- an .html file with the page's source, which you can open in VS Code and search for the element that "could not be found"

The file names come from the test name plus the date and time, for example test_login_with_logged_steps_20261116-141502.png. Characters that are awkward in file names, like the brackets in parametrized test names, are replaced with underscores.


PART 2 - LOGGING

print() works, but pytest hides its output, and it has no levels or timestamps. Python's logging module is built for this:

```python
import logging

logger = logging.getLogger(__name__)

def test_login_with_logged_steps(driver):
    logger.info("Opening the login page")
    login_page = LoginPage(driver).open()
    logger.info("Logging in as %s", VALID_USER)
    ...
```

- getLogger(__name__) creates a logger named after the file, so each message shows where it came from.
- The %s is filled in with the value after the comma. Logging prefers this to f-strings, but both work.

Levels, from least to most serious:

- DEBUG - fine detail, usually switched off
- INFO - normal steps ("Opening the login page")
- WARNING - something unexpected, but the test continues
- ERROR - something failed
- CRITICAL - something failed badly

By default, only WARNING and above are kept. To see INFO messages, ask for them.

Three ways to see the log:

```
python3 -m pytest FILES/ -v --log-level=INFO
```
INFO messages appear in the failure report, under "Captured log call", only for failed tests.

```
python3 -m pytest FILES/ -v --log-cli-level=INFO
```
Live log: every message is printed as it happens, for all tests.

```
python3 -m pytest FILES/ -v --log-file=test-run.log --log-file-level=INFO
```
Everything is written to test-run.log in the repo root, which you open in VS Code afterwards.

The options can be combined.


PART 3 - HTML REPORT

pytest-html turns a test run into a web page:

```
python3 -m pytest FILES/ --headless --html=report.html --self-contained-html
open report.html
```

- --html=report.html sets the file name.
- --self-contained-html puts everything in that one file. Without it, pytest-html also creates an assets/ folder next to it.
- open report.html opens it in your default browser (a Mac command).

The report shows a summary at the top, then one row per test with its result and duration. Click a failed test to see the error and any captured log messages. You can filter by result.

Each run overwrites report.html. To keep several, give each run a different file name.


THE FILES

- conftest.py - replaced: everything from Module 8, plus the hook and screenshots on failure
- mod9_debug_test.py - 3 tests: a login with logged steps, saving a screenshot by hand, checking the page source


WHY IT MATTERS / TRAPS (READ THIS PART!)

Trap 1 - Taking the screenshot after quit().
After drv.quit() there is no browser to photograph, and save_screenshot() raises an error. The screenshot must come before quit, which is why the fixture saves the evidence first and quits in the finally block.

Trap 2 - Screenshots for every test.
A screenshot per test slows every run and fills the folder with pictures nobody looks at. Save evidence only when a test fails.

Trap 3 - Committing screenshots.
A screenshot shows whatever was on the page. With a real app, that can include names, data or internal details, and in a public repo everyone can see it. The screenshots/ folder is in .gitignore for this reason. The same applies to report.html and test-run.log.

Trap 4 - Logging passwords.
Never log a password, a token or a full login form. Logs end up in files, reports and CI output. Log the username if it helps, never the password (same rule as Module 8 Trap 8).

Trap 5 - "My INFO messages do not show up".
The default level is WARNING, so INFO and DEBUG messages are dropped. Add --log-level=INFO, --log-cli-level=INFO or --log-file-level=INFO.

Trap 6 - Debugging with print().
pytest captures print() output and only shows it for failed tests (or with -s). It has no levels or timestamps, and you have to delete the lines afterwards. Logging can stay in the code: switch the level up or down instead.

Trap 7 - The screenshot shows the wrong moment.
The screenshot is taken in teardown, after the failure. Usually the page has not changed since, but if the failing step started a page change, the picture may show the next page. Read it together with the error message and the log.

Trap 8 - Forgetting breakpoint().
breakpoint() (from the "where to find errors" notes) stops the test and waits for you. Fine on your Mac, but a forgotten one makes the test wait forever, and on CI the job hangs until it times out.


HANDS-ON PRACTICE

Copy the new conftest.py over the old one first, and do the one-time setup.

1. Run the Module 9 tests with the live log:

```
python3 -m pytest FILES/mod9_debug_test.py -v --log-cli-level=INFO
```

   Expect 3 passed, with the log messages printed as each test runs. The screenshots/ folder is not created, because nothing failed.

2. Run everything headless with an HTML report:

```
python3 -m pytest FILES/ --headless --html=report.html --self-contained-html
open report.html
```

   Look at the summary and click a few tests. The Module 8 login test shows as skipped, unless TEST_USER and TEST_PASSWORD are set.

Break it on purpose (this step is MEANT to fail):

1. In mod9_debug_test.py, in test_login_with_logged_steps, change
   assert "You logged into a secure area!" in secure.flash_text()
   to
   assert "Welcome!" in secure.flash_text()
2. Run it headless, with the log and a report:

```
python3 -m pytest FILES/mod9_debug_test.py -v --headless --log-cli-level=INFO -k logged --html=report.html --self-contained-html
```

3. Collect the evidence:
   - the terminal: the E line, and the "Saved failure screenshot" message in the live log
   - the screenshots/ folder: open it with "open screenshots" and look at the .png. It shows the secure area page, so you know the login worked and only the expected text was wrong.
   - the .html file next to it: open it in VS Code and search for "secure area" to see the real banner text
   - report.html: open it and click the failed test
4. Change the line back and run again. It passes, and no new screenshot is saved.


MENTAL MODEL

- Test passes: nothing extra is saved.
- Test fails: screenshot + page HTML in screenshots/, error in the terminal.
- Logging: what the test was doing, step by step. Choose the level when you run.
- HTML report: the whole run in one page.
- Evidence stays out of Git.


FOR YOUR OWN APP LATER

- When a headless test fails on your dev site, look at the screenshot first. A login page, an error page or Chrome's "Privacy error" page often explains the failure straight away.
- Log the business steps ("Searching for model X", "Discarding column 123"), not every click. The log then reads like the test plan.
- Screenshots of a real app can contain real data. Keep them on your machine, and do not attach them to public issues or chats.


QUIZ (answers below - try before peeking)

1. Why does the fixture save the screenshot before calling drv.quit(), and why is quit() in a finally block?

2. Your test logs logger.info("Opening the login page"), but nothing appears when the test fails. Why, and how do you see it?

3. What does the pytest_runtest_makereport hook store, and why does the fixture need it?

4. Why only save screenshots when a test fails?

5. Why is screenshots/ in .gitignore?

6. Name one advantage of logging over print().

7. DevOps stretch question: a test fails on GitHub Actions and saves a screenshot. When the job ends, the runner is deleted, and the screenshot with it. How do you keep it? (Covered in Module 10. Just guess.)


ANSWERS

1. After quit() there is no browser left to take a screenshot of. The finally block makes sure the browser still closes even if saving the screenshot raises an error, so no Chrome windows are left behind.

2. The default log level is WARNING, so INFO messages are dropped. Run with --log-level=INFO (shown for failed tests), --log-cli-level=INFO (live) or --log-file-level=INFO together with --log-file.

3. It stores the result of each test phase on the test (rep_setup, rep_call, rep_teardown). The fixture's teardown code reads rep_call to find out whether the test failed, because a fixture has no other way of knowing.

4. Screenshots of passing tests slow down every run and fill the folder with pictures nobody needs. The evidence matters only when something went wrong.

5. Screenshots show whatever was on the page, which with a real app can include real data or internal details. In a public repo everyone could see them.

6. Any of: levels you can switch on and off without editing the code, timestamps and the file each message came from, output to a file, and pytest shows it in the failure report and the HTML report.

7. Upload the screenshots/ folder as a build artifact (GitHub's actions/upload-artifact action), usually only when the job failed. The files can then be downloaded from the workflow run page. In a public repo, artifacts can be downloaded by others, so the same care applies as with committing them.


End of Module 9. Next up: Module 10, running the tests on GitHub Actions on every push.