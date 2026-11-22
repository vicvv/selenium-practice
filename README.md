SELENIUM WITH PYTHON - A HANDS-ON LEARNING COURSE


WHAT THIS IS

Notes and practice code from learning browser test automation with Selenium and Python, from a first script to tests that run automatically on GitHub Actions.

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

- pip install -r requirements.txt installs the pinned versions of selenium, pytest and pytest-html, and also this repo's own package (selenium_practice), because of the -e . line at the end of requirements.txt.
- python3 -m pytest runs every test in tests/ and writes an HTML report to reports/.

Other ways to run:

```
python3 -m pytest --headless              # without a browser window
python3 -m pytest -m smoke                # smoke tests only
python3 -m pytest -k login                # only tests with "login" in the name
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
            pages/               page objects (Modules 5 and 6)
    tests/                       pytest tests, conftest.py, test data (Modules 4 to 10)
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

Five files must keep their exact names because the tools look for them: README.md, pyproject.toml, pytest.ini, requirements.txt and conft