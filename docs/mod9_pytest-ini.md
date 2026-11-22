SELENIUM WITH PYTHON - MODULE 9 EXTRA: THE PYTEST.INI FILE


WHAT IT IS

pytest.ini is a settings file for pytest. pytest reads it at the start of every run, so options you would otherwise type every time can be written there once.

- It lives in the repo root, next to tests/, src/ and docs/.
- It must keep this exact name, with no module prefix (like conftest.py).
- It holds no secrets, so it belongs in the repo. Anyone who clones the repo gets the same settings.


THE FILE

```
[pytest]
# Where the tests are, so "python3 -m pytest" works without tests/
testpaths = tests

# Options added to every run
addopts = -v -ra --strict-markers --html=report.html --self-contained-html

# Write a log file on every run (test-run.log is in .gitignore)
log_file = test-run.log
log_file_level = INFO
log_file_format = %(asctime)s %(levelname)s %(name)s: %(message)s
log_file_date_format = %H:%M:%S

# Labels you can put on tests (used in Module 10)
markers =
    smoke: quick checks of the most important features
```

Create or edit it in VS Code. Paste only the lines above into the file.


WHAT EACH SETTING DOES

[pytest]
  The first line. It tells pytest the settings below are for pytest.

testpaths = tests
  Where the tests live. From the repo root, "python3 -m pytest" is enough, without naming the folder. It also stops pytest from searching other folders, such as scripts/ or src/.

addopts
  Options added to every pytest command:
  - -v prints one line per test with PASSED or FAILED.
  - -ra adds a summary at the end listing every test that did not pass (failed, skipped or errored) and the reason.
  - --strict-markers makes a misspelled label, such as @pytest.mark.smok, stop with an error instead of being silently ignored.
  - --html=report.html --self-contained-html creates the HTML report on every run. tests/conftest.py then gives it a dated name in reports/ (see WHERE THE OUTPUT GOES).

log_file and log_file_level
  Write all INFO messages (and above) to test-run.log on every run. Each run overwrites the file.

log_file_format and log_file_date_format
  How each line in the log file looks: the time, the level, the file the message came from, and the message.

markers
  Labels you can put on tests with a decorator, for example @pytest.mark.smoke. Each label is on its own indented line, with a short description after the colon. "smoke" is used in Module 10 to run a small, quick set of tests.


WHAT PYTEST.INI DOES NOT DO: FINDING THE PAGE OBJECTS

The page objects live in the selenium_practice package (src/selenium_practice/pages/). Tests find them because the package is installed in the venv with pip install -e . (or pip install -r requirements.txt), not because of anything in pytest.ini.

So there is no pythonpath setting in this file, and none is needed. If a test fails with "No module named 'selenium_practice'", the fix is the install, not pytest.ini.


COMMANDS THAT GET SHORTER

Without pytest.ini:

```
python3 -m pytest tests/ -v -ra --html=report.html --self-contained-html
```

With it:

```
python3 -m pytest
```

You can still add options when you need them:

```
python3 -m pytest --headless                          # without a window
python3 -m pytest tests/mod8_settings_test.py         # one file
python3 -m pytest -k login                            # only matching tests
python3 -m pytest -m smoke                            # only smoke tests
python3 -m pytest --log-cli-level=INFO                # live log on screen as well
```

Options typed in the command are added after the ones in addopts. If the same option appears in both, the one in the command wins. For example, --html=report-module9.html saves the report under that name, and conftest.py leaves a name you typed alone.


WHERE THE OUTPUT GOES

Output is created relative to the folder you run pytest from. All the commands in these notes start in the repo root:

```
selenium-practice/
    docs/
    scripts/
    src/
    tests/
    reports/          <- a new dated report every run, e.g. report_20261122-135636.html
    screenshots/      <- only after a test fails
    test-run.log      <- every run, overwritten
    pytest.ini
```

- The line near the end of each run shows the exact report path.
- Open the newest report: open "$(ls -t reports/*.html | head -1)"
- Open the log: open test-run.log
- Clear old reports: rm -r reports

reports/, screenshots/ and test-run.log are in .gitignore, so they stay on your machine and do not appear in git status.


IF THE TESTS FOLDER IS RENAMED

testpaths must match the real folder name. If the tests ever move to another folder, for example tests/ui/, change the line:

```
testpaths = tests/ui
```

Several folders, separated by spaces:

```
testpaths = tests scripts_tests
```

If testpaths does not match, a plain "python3 -m pytest" does not run the tests you expect. Naming the folder in the command still works, because a path in the command overrides testpaths.

What else depends on the folder name:

- The commands in the notes and in docstrings (find them with git grep -n "tests/").
- The workflow file .github/workflows/mod10_selenium-tests.yml, which runs pytest on that folder.

What does not depend on it:

- tests/conftest.py finds the repo root from its own location (Path(__file__)), so screenshots/ and reports/ still land in the repo root.
- The Module 7 CSV file is found from the test file's own location.
- The page objects are imported from the installed package, so moving tests does not affect them.

Always move folders with git mv, so Git keeps each file's history.


WHY IT MATTERS / TRAPS (READ THIS PART!)

Trap 1 - A comment at the end of a line.
pytest.ini does not allow comments after a setting on the same line. The comment is read as part of the setting and breaks it. Put each comment on its own line, starting with #.

Trap 2 - --headless in addopts.
--headless is defined in tests/conftest.py, and pytest reads pytest.ini before that file is loaded. The run can stop with "unrecognized arguments: --headless". It would also hide the browser on every run. Type --headless in the command when you want it.

Trap 3 - "unrecognized arguments: --headless" with a short command.
python3 -m pytest --headless should work, because testpaths points pytest at tests/ and its conftest.py. If your pytest version still stops with this error, name the folder: python3 -m pytest tests/ --headless. That always works (Module 8, Trap 2).

Trap 4 - The file in the wrong place.
pytest looks for pytest.ini in the folder you run from and the folders above it. Inside tests/, it is found only when you run from tests/. Keep it in the repo root.

Trap 5 - Running pytest from another folder.
Output paths are relative to the folder you run from. Always run from the repo root, so reports, screenshots and the log land where .gitignore expects them.

Trap 6 - Expecting pytest.ini to fix imports.
"No module named 'selenium_practice'" means the package is not installed in the active venv. Activate the venv and run pip install -e . Adding a pythonpath line to pytest.ini would hide the problem instead of fixing it.

Trap 7 - Adding a marker without registering it.
With --strict-markers, a marker used on a test but not listed under markers stops the run with an error. Add every new label to pytest.ini first.

Trap 8 - Live log on every run.
log_cli = true prints every log message on screen for every run, and the output gets very long. Add --log-cli-level=INFO to the command only when you need it.


CHECK IT WORKS

```
cd ~/Documents/selenium-practice
source venv/bin/activate
python3 -m pytest
```

Near the top of the output you should see "configfile: pytest.ini" and "testpaths: tests". At the end: one line per test, a summary with the skip reason, and the path of the new report in reports/.