SELENIUM WITH PYTHON - A HANDS-ON LEARNING COURSE


WHAT THIS IS

Notes and practice code from learning browser test automation with Selenium and Python, from a first script to tests that run automatically on GitHub Actions.

Each module has a notes file with explanations, traps, a hands-on exercise and a quiz with answers, plus practice code you can run.

All practice code runs against public practice sites, so no account or special access is needed.


WHO IT IS FOR

- Testers and developers who are new to Selenium
- Some basic Python helps: variables, functions, if statements, loops
- You should be comfortable typing commands in a terminal

The course was done on a Mac, so the commands are for macOS (zsh). On Linux they are mostly the same. On Windows, several commands differ.


QUICK START

You need Python 3 and Google Chrome. Selenium 4.6 and later downloads the matching browser driver by itself.

```
git clone https://github.com/vicvv/selenium-practice.git
cd selenium-practice
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 -m pytest
```

Other ways to run:

```
python3 -m pytest --headless        # without a browser window
python3 -m pytest -m smoke          # smoke tests only
python3 -m pytest -k login          # only tests with "login" in the name
python3 FILES/mod1_locators.py      # a Module 1 to 3 script (these are not pytest tests)
```

The Module 8 login test reads its login from environment variables and skips if they are not set. To run it, use the practice site's public demo login:

```
export TEST_USER=tomsmith
export TEST_PASSWORD='SuperSecretPassword!'
```


REPO LAYOUT

```
selenium-practice/
    README.md              this file
    DOCS/                  notes for each module
    FILES/                 practice scripts, tests, page objects, conftest.py
    .github/workflows/     the GitHub Actions workflow (Module 10)
    pytest.ini             pytest settings
    requirements.txt       Python packages and versions
```

Created when tests run, and kept out of Git by .gitignore: screenshots/, reports/, test-run.log. The venv/ folder is also kept out of Git.

File names start with the module number and an underscore, for example mod5_pages.py. Underscores, not dashes, so that files can be imported by other files. Test files end in _test.py so pytest finds them.

Three files must keep their exact names because the tools look for them: conftest.py, pytest.ini and README.md.


THE MODULES

Module 0 - Setup and Git
  Notes: DOCS/mod0_setup-git.md
  Code:  FILES/mod0_first.py
  A Python virtual environment, installing Selenium, a first script that opens Chrome, Git and GitHub with an SSH key, .gitignore, everyday Git commands and common fixes.

Module 1 - Locators
  Notes: DOCS/mod1_locators.md
  Code:  FILES/mod1_locators.py
  Finding elements by ID, name, CSS selector, XPath and more. find_element vs find_elements. Choosing locators that do not break.

Module 2 - Waits
  Notes: DOCS/mod2_waits.md
  Code:  FILES/mod2_waits.py
  Explicit waits with WebDriverWait and expected conditions. Why time.sleep() and implicit waits lead to flaky tests.

Module 3 - Browser interactions
  Notes: DOCS/mod3_interactions.md
  Code:  FILES/mod3_interactions.py
  Typing, clearing, clicking, keyboard keys, select dropdowns, checkboxes and radio buttons. Waiting for a change to happen before checking it.

Module 4 - Assertions and pytest
  Notes: DOCS/mod4_pytest.md
  Code:  FILES/mod4_basics_test.py, FILES/conftest.py
  Turning scripts into tests that pass or fail. assert, how pytest finds tests, fixtures for setup and teardown, reading failure output, keeping tests independent.

Module 5 - Page Object Model
  Notes: DOCS/mod5_page-objects.md
  Code:  FILES/mod5_pages.py, FILES/mod5_login_test.py
  One class per page holding its locators and actions. A base page with shared helpers. Methods that return the next page. Keeping locators out of tests.

Module 6 - Tricky elements
  Notes: DOCS/mod6_tricky-elements.md
  Code:  FILES/mod6_pages.py, FILES/mod6_tricky_test.py
  JavaScript alerts, iframes and nested frames, multiple tabs and windows, file uploads using pytest's tmp_path.

Module 7 - Data-driven tests
  Notes: DOCS/mod7_data-driven.md, DOCS/mod7_where-to-find-errors.md
  Code:  FILES/mod7_login_data_test.py, FILES/mod7_login_cases.csv
  pytest parametrize, readable case ids, test data from a CSV file, choosing good test cases, and where to look when a test fails.

Module 8 - Headless mode, Chrome options and credentials
  Notes: DOCS/mod8_headless-options.md
  Code:  FILES/mod8_settings_test.py
  Headless Chrome, a fixed window size, a custom --headless option, certificate warnings, passwords in environment variables, and skipping a test with a clear reason.

Module 9 - Debugging
  Notes: DOCS/mod9_debugging.md, DOCS/mod9_pytest-ini.md
  Code:  FILES/mod9_debug_test.py, pytest.ini
  A screenshot and the page HTML saved automatically when a test fails, logging, HTML reports with dated names, and default options in pytest.ini.

Module 10 - GitHub Actions
  Notes: DOCS/mod10_github-actions.md
  Code:  .github/workflows/mod10_selenium-tests.yml, FILES/mod10_smoke_test.py
  Running the tests on every push, repository secrets, smoke tests with markers, and saving reports and screenshots as artifacts.


HOW EACH NOTES FILE IS ORGANIZED

- Goal
- Explanation with examples
- Why it matters / traps: the mistakes that cause most problems
- Hands-on practice, including a "break it on purpose" step that shows what a failure looks like
- Mental model: a short summary
- Quiz, with answers at the end


OTHER TOPICS COVERED ALONG THE WAY

Python

- python and python3, pip and pip3 on a Mac
- virtual environments and requirements.txt
- decorators: @pytest.fixture, @pytest.mark.parametrize, @property
- classes and inheritance (page objects)
- try, except and finally
- why a dash in a file name breaks an import
- pathlib and Path(__file__) for paths that work on any machine
- the csv and logging modules
- breakpoint() to pause a test

pytest

- how pytest finds tests, and fixtures with yield
- the built-in fixtures tmp_path and request
- hooks: pytest_addoption, pytest_configure, pytest_runtest_makereport
- markers and --strict-markers
- command options: -v, -k, -m, -x, --lf, -ra, -s
- settings in pytest.ini

Git and GitHub

- SSH keys instead of tokens
- .gitignore, and checking it with git status --ignored
- renaming many files with git mv, a shell loop and sed (on a Mac: sed -i '')
- "divergent branches", and git pull --rebase
- why editing on the GitHub website and locally at the same time causes conflicts
- repository secrets and artifacts
- deleting a file does not remove it from Git history

Shell

- heredocs: cat > file << 'EOF', and the difference between quoted and unquoted EOF
- export and environment variables, and read -s for passwords
- tee to save output to a file, grep -n to find line numbers

Testing practice

- where expected results come from: the specification, manual exploration, and confirming with developers
- checking stable signals such as the URL or the message type, not only exact wording
- snapshot (golden master) testing, and its limits
- breaking a test on purpose to prove it can fail
- smoke tests vs the full set
- keeping passwords, real data and screenshots out of a public repo
- designing test cases: functional, negative, edge and boundary, network and resilience
- an overview of test management tools such as TestRail, Qase, Zephyr and Xray


NOT COVERED - IDEAS FOR NEXT STEPS

More Selenium

- ActionChains: hover, drag and drop, right-click, double-click
- running JavaScript with execute_script, and scrolling
- elements inside a shadow DOM
- relative locators (above, below, near), added in Selenium 4
- cookies and local storage, and reusing a logged-in session
- other browsers: Firefox, Edge, Safari
- Selenium Grid and remote browsers
- WebDriver BiDi: reading network traffic and console logs

Scaling and reliability

- running tests in parallel with pytest-xdist
- retrying flaky tests with pytest-rerunfailures, and why retries can hide real problems
- running Selenium in Docker
- self-hosted runners and company CI systems, for apps on a private network

Other kinds of testing

- API testing (for example the requests library, or Postman)
- accessibility testing (for example axe)
- visual regression testing
- performance and load testing
- mobile apps with Appium
- BDD with Gherkin (for example pytest-bdd)

Other tools

- Playwright and Cypress, newer browser automation tools
- Selenium in JavaScript: the concepts in this course carry over
- reporting tools such as Allure


RESOURCES

Links may move over time. If one does not work, search for the page title.

Selenium

- Selenium documentation: https://www.selenium.dev/documentation/
- Selenium Python API reference: https://www.selenium.dev/selenium/docs/api/py/
- Selenium's practice web form (Module 1): https://www.selenium.dev/selenium/web/web-form.html

Practice sites

- The Internet (Modules 2 to 10): https://the-internet.herokuapp.com/
- badssl.com, for certificate errors (Module 8): https://badssl.com/

pytest

- pytest documentation: https://docs.pytest.org/
- pytest-html: https://pytest-html.readthedocs.io/
- pytest-xdist: https://pytest-xdist.readthedocs.io/

Python

- Python documentation: https://docs.python.org/3/
- venv: https://docs.python.org/3/library/venv.html
- Logging HOWTO: https://docs.python.org/3/howto/logging.html
- csv module: https://docs.python.org/3/library/csv.html

Git and GitHub

- Pro Git, a free book: https://git-scm.com/book
- Connecting to GitHub with SSH: https://docs.github.com/en/authentication/connecting-to-github-with-ssh
- GitHub Actions documentation: https://docs.github.com/en/actions

Patterns and other tools

- Page Object, by Martin Fowler: https://martinfowler.com/bliki/PageObject.html
- Playwright for Python: https://playwright.dev/python/


ABOUT THE PRACTICE SITES

The practice sites are run by other people and are sometimes down. If every test fails with a timeout at its first step, open the site in your browser. If it does not load, wait and try again later.

Only the sites' public demo login is used. No real data is used anywhere in this repo.