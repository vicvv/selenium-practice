SELENIUM WITH PYTHON - A HANDS-ON LEARNING COURSE


WHAT THIS IS

Notes and practice code from learning browser test automation with Selenium and Python, from a first script to tests that run automatically on GitHub Actions, ending with a capstone project built from acceptance criteria alone.

Each module has a notes file with explanations, traps, a hands-on exercise and a quiz with answers, plus practice code you can run.

The repo is also an installable Python package (selenium_practice) that holds the page objects, so the tests import them like any other package.

All practice code runs against public practice sites, so no account or special access is needed.


WHO IT IS FOR

- Testers and developers who are new to Selenium
- Some basic Python helps: variables, functions, if statements, loops
- You should be comfortable typing commands in a terminal

The course was done on a Mac, so the commands are for macOS (zsh). On Linux they are mostly the same. On Windows, see WINDOWS below.


QUICK START

You need Python 3.10 or later, Git and Google Chrome. Selenium 4.6 and later downloads the matching browser driver by itself.

```
git clone https://github.com/vicvv/selenium-practice.git
cd selenium-practice
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 -m pytest
```

- pip install -r requirements.txt installs the pinned versions of selenium, pytest, pytest-html and pytest-xdist, and also this repo's own package (selenium_practice), because of the -e . line at the end of requirements.txt.
- python3 -m pytest runs every test in tests/ and writes an HTML report to reports/.

Other ways to run:

```
python3 -m pytest --headless              # without a browser window
python3 -m pytest -m smoke                # smoke tests only
python3 -m pytest -k login                # only tests with "login" in the name
python3 -m pytest -n 4                    # four tests at a time (Module 10)
python3 scripts/mod1_locators.py          # a Module 0 to 3 script (these are not pytest tests)
```

The Module 8 login test reads its login from environment variables and skips if they are not set. To run it, use the practice site's public demo login:

```
export TEST_USER=tomsmith
export TEST_PASSWORD='SuperSecretPassword!'
```


WINDOWS

Use PowerShell. Create and activate the venv with:

```
python -m venv venv
venv\Scripts\Activate.ps1
```

- If PowerShell says running scripts is disabled, run this once, then activate again: Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
- Set environment variables with $env:TEST_USER = "tomsmith" instead of export.
- The pip and pytest commands are the same. Use python instead of python3.


REPO LAYOUT

```
selenium-practice/
    src/
        selenium_practice/       the package: code the tests import
            pages/               page objects (Modules 5, 6, 11, 12 and 13)
    tests/                       pytest tests, conftest.py, test data (Modules 4 to 13)
    scripts/                     plain scripts for Modules 0 to 3 (run with python3)
    docs/                        notes for each module
    .github/workflows/           the GitHub Actions workflow (Module 10)
    pyproject.toml               describes the package, so pip can install it
    pytest.ini                   pytest settings
    requirements.txt             pinned versions, plus the package itself
    README.md                    this file
```

Created when tests run, and kept out of Git by .gitignore: screenshots/, reports/, test-run.log. The venv/ folder and the selenium_practice.egg-info/ folder (created by the editable install) are also kept out of Git.


INSTALLING THE PACKAGE

The page objects live in a real Python package. pyproject.toml describes it, and the code is in src/selenium_practice/. There are three ways to install it.

1. Editable, for working on the course (the normal way). Run it from the repo root, with the venv active:

```
pip install -e .
```

- The dot means "the package in this folder".
- -e (editable) means Python reads the files straight from src/, so a change to a page object takes effect immediately, with no reinstall.
- pip install -r requirements.txt does this too, because its last line is -e .

2. A normal, fixed copy, from the repo folder:

```
pip install .
```

Python gets a copy of the package as it is now. Later changes to src/ are not picked up until you install again.

3. Straight from GitHub, into another project, without cloning:

```
pip install "git+https://github.com/vicvv/selenium-practice.git"
```

Add @main or a tag name at the end of the address to choose a version.

What gets installed: the selenium_practice package (the page objects) and Selenium, which pyproject.toml lists as a dependency. The tests, scripts and notes stay in the repo.

Tests import the page objects like this:

```python
from selenium_practice.pages.mod5_pages import LoginPage
```

Check the package is installed:

```
python -c "import selenium_practice.pages.mod5_pages; print('import OK')"
pip show selenium-practice
```

The project name is selenium-practice, with a dash, but the import name is selenium_practice, with an underscore, because Python cannot import a name with a dash. To remove it: pip uninstall selenium-practice


NAMING

- File names start with the module number and an underscore, for example mod5_pages.py. Underscores, not dashes, so that files can be imported.
- Test files end in _test.py so pytest finds them.
- Notes are docs/modN_topic.md.

Five files must keep their exact names because the tools look for them: README.md, pyproject.toml, pytest.ini, requirements.txt and conftest.py.


THE MODULES AT A GLANCE

- Module 0 - Setup and Git
- Module 1 - Locators
- Module 2 - Waits and stale elements
- Module 3 - Browser interactions
- Module 4 - Assertions and pytest
- Module 5 - Page Object Model
- Module 6 - Tricky elements
- Module 7 - Data-driven tests
- Module 8 - Headless mode, Chrome options and credentials
- Module 9 - Debugging
- Module 10 - GitHub Actions and parallel runs
- Module 11 - Advanced interactions
- Module 12 - Web tables and dynamic lists
- Module 13 - Capstone project

Modules 0 to 3 are plain scripts you run with python3. From Module 4 on, everything is a pytest test.


THE MODULES

Module 0 - Setup and Git
  Notes: docs/mod0_setup-git.md
  Code:  scripts/mod0_first.py
  A Python virtual environment, installing Selenium, a first script that opens Chrome, Git and GitHub with an SSH key, .gitignore, everyday Git commands and common fixes.

Module 1 - Locators
  Notes: docs/mod1_locators.md
  Code:  scripts/mod1_locators.py
  Finding elements by ID, name, CSS selector, XPath and more. find_element vs find_elements. Choosing locators that do not break.

Module 2 - Waits and stale elements
  Notes: docs/mod2_waits.md
  Code:  scripts/mod2_waits.py
  Explicit waits with WebDriverWait and expected conditions. Why time.sleep() and implicit waits lead to flaky tests. StaleElementReferenceException: what it means when the page redraws an element, and how to avoid it by finding the element again instead of holding on to it.

Module 3 - Browser interactions
  Notes: docs/mod3_interactions.md
  Code:  scripts/mod3_interactions.py, scripts/mod3_interactions_slow.py
  Typing, clearing, clicking, keyboard keys, select dropdowns, checkboxes and radio buttons. Waiting for a change to happen before checking it.

Module 4 - Assertions and pytest
  Notes: docs/mod4_pytest.md
  Code:  tests/mod4_basics_test.py, tests/conftest.py
  Turning scripts into tests that pass or fail. assert, how pytest finds tests, fixtures for setup and teardown, reading failure output, keeping tests independent.

Module 5 - Page Object Model
  Notes: docs/mod5_page-objects.md
  Code:  src/selenium_practice/pages/mod5_pages.py, tests/mod5_login_test.py
  One class per page holding its locators and actions. A base page with shared helpers. Methods that return the next page. Keeping locators out of tests.

Module 6 - Tricky elements
  Notes: docs/mod6_tricky-elements.md
  Code:  src/selenium_practice/pages/mod6_pages.py, tests/mod6_tricky_test.py
  JavaScript alerts, iframes and nested frames, multiple tabs and windows, file uploads using pytest's tmp_path, and elements inside a shadow DOM (CSS selectors work inside a shadow root, XPath does not).

Module 7 - Data-driven tests
  Notes: docs/mod7_data-driven.md, docs/mod7_where-to-find-errors.md
  Code:  tests/mod7_login_data_test.py, tests/mod7_login_cases.csv, tests/mod7_search_cases.json
  pytest parametrize, readable case ids, test data from a CSV file, JSON for data with a nested structure, choosing good test cases, and where to look when a test fails.

Module 8 - Headless mode, Chrome options and credentials
  Notes: docs/mod8_headless-options.md, docs/mod8_real-app-checklist.md
  Code:  tests/mod8_settings_test.py
  Headless Chrome, a fixed window size, a custom --headless option, certificate warnings, passwords in environment variables, skipping a test with a clear reason, and a checklist before automating a real app.

Module 9 - Debugging
  Notes: docs/mod9_debugging.md, docs/mod9_pytest-ini.md
  Code:  tests/mod9_debug_test.py, pytest.ini
  A screenshot and the page HTML saved automatically when a test fails, logging, HTML reports with dated names, and default options in pytest.ini.

Module 10 - GitHub Actions and parallel runs
  Notes: docs/mod10_github-actions.md, docs/mod10_parallel.md
  Code:  .github/workflows/mod10_selenium-tests.yml, tests/mod10_smoke_test.py
  Running the tests on every push, repository secrets, smoke tests with markers, saving reports and screenshots as artifacts, and running tests in parallel with pytest-xdist (including what has to change in conftest.py first).

Module 11 - Advanced interactions
  Notes: docs/mod11_advanced-interactions.md
  Code:  src/selenium_practice/pages/mod11_pages.py, tests/mod11_actions_test.py
  ActionChains: hover menus, right-click, double-click and key combinations. Scrolling to an element and loading content that only appears when you scroll. Running JavaScript with execute_script, and why HTML5 drag and drop often needs it.
  Practice pages: /hovers, /context_menu, /infinite_scroll, /drag_and_drop

Module 12 - Web tables and dynamic lists
  Notes: docs/mod12_tables.md
  Code:  src/selenium_practice/pages/mod12_pages.py, tests/mod12_tables_test.py
  Finding a row by the text in one of its cells, acting on a button in that row, reading a whole column, checking sorting, counting rows, and waiting for a list to finish updating.
  Practice pages: /tables, /challenging_dom

Module 13 - Capstone project
  Notes: docs/mod13_capstone.md
  Code:  src/selenium_practice/pages/mod13_pages.py, tests/mod13_capstone_test.py
  An end-to-end shopping flow on a public demo shop (saucedemo.com), built from acceptance criteria only, with no starter code. It uses page objects, fixtures, data-driven cases, a headless run and the CI workflow.


HOW EACH NOTES FILE IS ORGANIZED

- Goal
- Explanation with examples
- Why it matters / traps: the mistakes that cause most problems
- Hands-on practice, including a "break it on purpose" step that shows what a failure looks like
- Mental model: a short summary
- For your own app later: how the module applies to a real project
- Quiz, with answers at the end


OTHER TOPICS COVERED ALONG THE WAY

Python

- python and python3, pip and pip3 on a Mac
- virtual environments and requirements.txt
- packaging: pyproject.toml, the src/ layout, editable installs
- decorators: @pytest.fixture, @pytest.mark.parametrize, @property
- classes and inheritance (page objects)
- try, except and finally
- why a dash in a file name breaks an import
- pathlib and Path(__file__) for paths that work on any machine
- the csv, json and logging modules
- breakpoint() to pause a test

pytest

- how pytest finds tests, and fixtures with yield
- the built-in fixtures tmp_path and request
- hooks: pytest_addoption, pytest_configure, pytest_runtest_makereport
- markers and --strict-markers
- command options: -v, -k, -m, -n, -x, --lf, -ra, -s
- settings in pytest.ini

Git and GitHub

- SSH keys instead of tokens
- .gitignore, and checking it with git status --ignored
- moving and renaming files with git mv, so history is kept
- "divergent branches", and git pull --rebase
- why editing on the GitHub website and locally at the same time causes conflicts
- repository secrets and artifacts
- deleting a file does not remove it from Git history

Shell

- heredocs: cat > file << 'EOF', and the difference between quoted and unquoted EOF
- export and environment variables, and read -s for passwords
- tee to save output to a file, grep -n to find line numbers
- sed -i '' on a Mac (BSD sed) vs sed -i on Linux

Testing practice

- where expected results come from: the specification, manual exploration, and confirming with developers
- checking stable signals such as the URL or the message type, not only exact wording
- snapshot (golden master) testing, and its limits
- breaking a test on purpose to prove it can fail
- smoke tests vs the full set
- browser pop-ups (such as a password warning) that cover the page and swallow clicks
- keeping passwords, real data and screenshots out of a public repo


NOT COVERED - IDEAS FOR NEXT STEPS

More Selenium

- relative locators (above, below, near), added in Selenium 4
- cookies and local storage, and reusing a logged-in session
- other browsers: Firefox, Edge, Safari
- Selenium Grid and remote browsers

Scaling and reliability

- retrying flaky tests with pytest-rerunfailures, and why retries can hide real problems
- running Selenium in Docker
- self-hosted runners and company CI systems, for apps on a private network
- a linter and formatter, such as Ruff, to keep test code tidy in CI

Other kinds of testing and tools

- API testing (for example the requests library)
- accessibility, visual regression and performance testing
- Playwright and Cypress, newer browser automation tools
- reporting tools such as Allure


RESOURCES

Links may move over time. If one does not work, search for the page title.

- Selenium documentation: https://www.selenium.dev/documentation/
- Selenium Python API reference: https://www.selenium.dev/selenium/docs/api/py/
- pytest documentation: https://docs.pytest.org/
- pytest-html: https://pytest-html.readthedocs.io/
- pytest-xdist: https://pytest-xdist.readthedocs.io/
- Python venv: https://docs.python.org/3/library/venv.html
- Python packaging guide (pyproject.toml, editable installs): https://packaging.python.org/
- Pro Git, a free book: https://git-scm.com/book
- Connecting to GitHub with SSH: https://docs.github.com/en/authentication/connecting-to-github-with-ssh
- GitHub Actions documentation: https://docs.github.com/en/actions
- Page Object, by Martin Fowler: https://martinfowler.com/bliki/PageObject.html


ABOUT THE PRACTICE SITES

- Selenium's practice web form (Module 1): https://www.selenium.dev/selenium/web/web-form.html
- The Internet (Modules 2 to 12): https://the-internet.herokuapp.com/
- badssl.com, for certificate errors (Module 8): https://badssl.com/
- Sauce Demo, for the capstone (Module 13): https://www.saucedemo.com/

These sites are run by other people and are sometimes down. If every test fails with a timeout at its first step, open the site in your browser. If it does not load, wait and try again later.

Only the sites' public demo logins are used. Chrome may warn that a demo password appears in a data breach. Those passwords are public on purpose, so the warning is expected. No real data is used anywhere in this repo.