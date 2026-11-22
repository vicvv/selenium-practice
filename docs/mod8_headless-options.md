SELENIUM WITH PYTHON - MODULE 8: HEADLESS MODE, CHROME OPTIONS AND CREDENTIALS


GOAL

Control how the browser starts, and keep passwords out of the code. Three topics:

- Headless mode: Chrome runs without a window. Needed on machines with no screen, such as GitHub Actions runners.
- Chrome options: window size and certificate warnings.
- Credentials: tests read usernames and passwords from environment variables, never from the code.

All of this lives in conftest.py, so the tests themselves hardly change.


PART 1 - CHROME OPTIONS

An Options object holds the settings Chrome starts with. You build it, then pass it to webdriver.Chrome():

```python
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

opts = Options()
opts.add_argument("--headless=new")         # no window
opts.add_argument("--window-size=1280,800") # fixed window size
opts.accept_insecure_certs = True           # ignore certificate errors (see Part 3)

driver = webdriver.Chrome(options=opts)
```

- add_argument() passes a command-line switch to Chrome.
- accept_insecure_certs is a setting on the Options object, not a switch.

Options only take effect when the browser starts. Changing them later does nothing to a browser that is already open.


PART 2 - HEADLESS MODE

Headless Chrome is real Chrome: it loads pages, runs JavaScript, clicks and types exactly the same way. It just does not draw a window.

Why use it:

- Machines with no screen (GitHub Actions, servers) cannot open a window at all. Without headless, the test crashes on webdriver.Chrome(). That was the Module 4 stretch question.
- It does not cover your screen while tests run.
- It is often a little faster.

The cost: you cannot watch it. When a headless test fails, you only have the output. Module 9 adds screenshots for that.

Always set a window size in headless mode. Headless Chrome starts with a small default window, so a page can switch to its mobile layout or hide elements, and a test that passes with a window fails without one.


TURNING HEADLESS ON FROM THE COMMAND LINE

conftest.py adds a --headless option to pytest:

```python
def pytest_addoption(parser):
    parser.addoption(
        "--headless",
        action="store_true",
        default=False,
        help="Run Chrome without a visible window",
    )
```

- pytest_addoption is a hook: a function with a special name that pytest calls while starting up. This one adds a new command-line option.
- action="store_true" means the option takes no value. Present means True, absent means False.

The fixture reads the option through request, a built-in pytest fixture that gives information about the current test run:

```python
@pytest.fixture
def driver(request):
    headless = request.config.getoption("--headless")
    drv = webdriver.Chrome(options=build_chrome_options(headless))
    yield drv
    drv.quit()
```

Now the same tests run either way:

```
python3 -m pytest tests/ -v               # with a window (default)
python3 -m pytest tests/ -v --headless    # without a window
```


PART 3 - CERTIFICATE WARNINGS

HTTPS sites prove who they are with a certificate. If the certificate is expired, self-signed or issued by an authority the computer does not trust, Chrome shows a "Your connection is not private" page instead of the site. The page title becomes "Privacy error".

Selenium does not raise an error when that happens. driver.get() returns normally, but the browser is showing Chrome's warning page, so every locator after that fails.

Internal dev and test sites sometimes use certificates like this. accept_insecure_certs = True tells Chrome to skip the warning and load the site.

Use it carefully:

- It switches off a real security check. Use it only for sites you know and trust, such as your own dev environment.
- Do not turn it on for every test. In this module it has its own fixture, insecure_driver, so only tests that ask for it get it.
- A certificate problem on a production site is a real bug. A test should catch it, not hide it.


PART 4 - CREDENTIALS IN ENVIRONMENT VARIABLES

Real passwords must never be in the code, in a data file or in a commit. In a public repo, anyone can read them, and deleting them later does not remove them from Git history.

Instead, the test reads them from environment variables: values set in the terminal that programs started from that terminal can read.

Set them in the terminal (venv active, before running pytest):

```
export TEST_USER=tomsmith
export TEST_PASSWORD='SuperSecretPassword!'
```

Read them in Python:

```python
import os

user = os.environ.get("TEST_USER")          # None if it is not set
password = os.environ.get("TEST_PASSWORD")
```

Check, remove:

```
echo $TEST_USER                    # shows the value
unset TEST_USER TEST_PASSWORD      # removes both
```

The single quotes around the password keep it exactly as typed. Without them, the shell may change special characters such as $ or ! before Python sees them. Same idea as the quoted 'EOF' in a heredoc.

The practice site's demo login is public, so it is safe here. The point is the habit: when you test a real app, only the values change, not the code.


SKIPPING A TEST WHEN THE CREDENTIALS ARE MISSING

If the variables are not set, the test should not fail with a confusing error. It should skip and say why:

```python
def get_credentials():
    user = os.environ.get("TEST_USER")
    password = os.environ.get("TEST_PASSWORD")
    if not user or not password:
        pytest.skip("Set TEST_USER and TEST_PASSWORD to run this test")
    return user, password
```

pytest.skip() stops the test and reports it as SKIPPED, not FAILED. To see the reason in the summary, add -rs:

```
python3 -m pytest tests/mod8_settings_test.py -v -rs
```


THE FILES

- conftest.py - replaced: adds --headless, a fixed window size, and an insecure_driver fixture. The driver fixture works as before.
- mod8_settings_test.py - 4 tests: window size, certificate blocked, certificate accepted, login with credentials from environment variables

Add .env to .gitignore now, so a file holding secrets can never be committed by accident (a .env file is a common way to store environment variables; you may use one later):

```
echo ".env" >> .gitignore
```


WHY IT MATTERS / TRAPS (READ THIS PART!)

Trap 1 - Headless with no window size.
The small default window can trigger a mobile layout or hide elements. The test passes when you watch it and fails headless. Always set --window-size.

Trap 2 - "unrecognized arguments: --headless".
pytest only reads pytest_addoption from conftest.py files it loads at startup. With tests/ on the command line, it loads tests/conftest.py and the option works. Plain python3 -m pytest --headless from the repo root does not load it, and pytest stops with this error. Always include tests/ (or a file inside it).

Trap 3 - accept_insecure_certs for everything.
Turning it on in every fixture hides real certificate problems. Keep it in a separate fixture and use it only where you need it.

Trap 4 - Thinking driver.get() failed on a certificate error.
It does not fail. The browser shows "Privacy error" and the next locator times out. If every test on a site times out at the first step, check the page title for "Privacy error".

Trap 5 - Forgetting export.
TEST_USER=tomsmith (without export) creates a shell variable that programs started from the terminal cannot see. Python gets None, and the test is skipped. Use export.

Trap 6 - Variables disappear in a new terminal.
Like venv activation, export only lasts for the current terminal window. A new tab or window means setting them again.

Trap 7 - Passwords in shell history.
Every command you type is saved in your shell history file (~/.zsh_history on a Mac). An export with a real password stays there. For real passwords, type it without it appearing on screen or in history:

```
read -s TEST_PASSWORD
export TEST_PASSWORD
```

read -s waits for you to type and does not show the characters. Press Enter when done.

Trap 8 - Printing or asserting on a password.
pytest prints the values in a failed assert, and print() output can end up in logs. On GitHub Actions in a public repo, logs can be visible to others. Never print a password or use it in an assert.


HANDS-ON PRACTICE

Copy the new conftest.py over the old one first. Then:

1. Run the Module 8 tests without any variables set:

```
python3 -m pytest tests/mod8_settings_test.py -v -rs
```

   Expect 3 passed and 1 skipped. The skipped one is the login test, with the reason shown.

2. Set the variables and run again:

```
export TEST_USER=tomsmith
export TEST_PASSWORD='SuperSecretPassword!'
python3 -m pytest tests/mod8_settings_test.py -v
```

   Expect 4 passed.

3. Run everything headless:

```
python3 -m pytest tests/ -v --headless
```

   No windows open, and every module's tests still pass. That is roughly how they would run on GitHub Actions.

Break it on purpose (this step is MEANT to fail):

1. Set a wrong password:

```
export TEST_PASSWORD=wrong
python3 -m pytest tests/mod8_settings_test.py -v -k env
```

2. The test fails with a TimeoutException from login_as() in mod5_pages.py: the login fails, so the URL never changes to /secure.
3. Notice that the failure output does not show the password, because the test never prints it or asserts on it (Trap 8).
4. Set it back:

```
export TEST_PASSWORD='SuperSecretPassword!'
```

The two certificate tests depend on badssl.com, a public site. If it is down, those two tests fail even though your code is fine. If your Chrome is set to another language, the "Privacy error" title is translated and the blocked-certificate test fails.


export TEST_USER=tomsmith

MENTAL MODEL

- Options: set before the browser starts, in conftest.py.
- Headless: the same tests, no window. Always with a window size.
- Insecure certificates: only in a separate fixture, only for trusted dev sites.
- Credentials: set in the terminal, read with os.environ, never in the repo.
- Missing credentials: skip with a clear reason, not a confusing failure.


FOR YOUR OWN APP LATER

- On a company-managed computer, the company's certificates are often already trusted. Try your dev site without accept_insecure_certs first, and only use insecure_driver if you get "Privacy error".
- Ask for a dedicated test account, and store its password only in environment variables (or a .env file that is in .gitignore).
- Logins with multi-factor authentication usually cannot be automated. Ask whether the test account can be set up without it, for the dev environment only.
- If the dev site needs a VPN, connect before running tests. Selenium uses your computer's network like any other program.


QUIZ (answers below - try before peeking)

1. Your tests pass with a window but fail with --headless. The failures are about elements not being found. What is the most likely cause, and the fix?

2. You run python3 -m pytest --headless from the repo root and get "unrecognized arguments: --headless". Why, and how do you run it correctly?

3. Every test against a site times out on its first locator, and the page title is "Privacy error". What is happening, and what can you do?

4. Why does accept_insecure_certs have its own fixture instead of being on for every test?

5. You typed TEST_USER=tomsmith and TEST_PASSWORD=secret, then ran pytest. The login test was skipped. What did you forget?

6. Why is pytest.skip() better than letting the test run without credentials?

7. DevOps stretch question: on GitHub Actions there is no terminal where you can type export. How do you give TEST_PASSWORD to the tests there without putting it in the repo? (Covered in Module 10. Just guess.)


ANSWERS

1. No window size was set, so headless Chrome used its small default window. The page switched to a smaller layout or hid elements. Set --window-size in the Chrome options.

2. pytest only reads pytest_addoption from conftest.py files it loads at startup. Without tests/ on the command line, tests/conftest.py is not loaded, so pytest does not know the option. Run python3 -m pytest tests/ --headless.

3. The site's certificate is not trusted, so Chrome shows its warning page instead of the site, and no locator matches. For a trusted dev site, use a browser started with accept_insecure_certs (the insecure_driver fixture). Better, if possible: have the certificate fixed, or install the company certificate so the computer trusts it.

4. It switches off a security check. On for every test, it would hide real certificate problems, including on sites where a bad certificate is a real bug. A separate fixture limits it to the tests that need it.

5. export. Without it, the shell keeps the values to itself, so Python reads None and the test skips.

6. A skip says clearly what is missing. Running without credentials would fail with a confusing error (a timeout, or None being typed into a field), and it would look like a bug in the app.

7. Store the password as a repository secret in the GitHub repo settings. The workflow file passes it to the tests as an environment variable, for example env: TEST_PASSWORD: ${{ secrets.TEST_PASSWORD }}. The test code reads os.environ exactly as it does on your Mac, and the secret never appears in the repo.


End of Module 8. Next up: Module 9, debugging (screenshots on failure, logging, and HTML reports).