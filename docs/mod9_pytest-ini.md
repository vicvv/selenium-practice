SELENIUM WITH PYTHON - MODULE 9 EXTRA: THE PYTEST.INI FILE


WHAT IT IS

pytest.ini is a settings file for pytest. pytest reads it at the start of every run, so options you would otherwise type every time can be written there once.

- It lives in the repo root, next to tests/ and docs/, not inside tests/.
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

To create it from the terminal instead of VS Code:

```
cd ~/Documents/selenium-practice
cat > pytest.ini << 'EOF'
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
EOF
```

The quoted 'EOF' keeps the %(asctime)s parts exactly as written.


WHAT EACH SETTING DOES

[pytest]
  The first line. It tells pytest the settings below are for pytest.

testpaths = tests
  Where the tests live. From the repo root, "python3 -m pytest" is enough, without tests/. It also stops pytest from searching other folders.

addopts
  Options added to every pytest command:
  - -v prints one line per test with PASSED or FAILED.
  - -ra adds a summary at the end listing every test that did not pass (failed, skipped or errored) and the reason. It replaces -rs.
  - --strict-markers makes a misspelled label, such as @pytest.mark.smok, stop with an error instead of being silently ignored.
  - --html=report.html --self-contained-html creates the HTML report on every run.

log_file and log_file_level
  Write all INFO messages (and above) to test-run.log on every run. Each run overwrites the file.

log_file_format and log_file_date_format
  How each line in the log file looks: the time, the level, the file the message came from, and the message.

markers
  Labels you can put on tests with a decorator, for example @pytest.mark.smoke. Each label is on its own indented line, with a short description after the colon. "smoke" is used in Module 10 to run a small, quick set of tests.


COMMANDS THAT GET SHORTER

Before:

```
python3 -m pytest tests/ -v -rs --html=report.html --self-contained-html
```

Now:

```
python3 -m pytest
```

You can still add options when you need them, and the old commands in the notes still work:

```
python3 -m pytest --headless                      # without a window
python3 -m pytest tests/mod8_settings_test.py     # one file
python3 -m pytest -k login                        # only matching tests
python3 -m pytest --log-cli-level=INFO            # live log on screen as well
```

Options typed in the command are added after the ones in addopts. If the same option appears in both, the one in the command wins. For example, --html=report-module9.html saves the report under that name instead.


WHERE THE OUTPUT GOES

Both files are created in the folder you run pytest from. All the commands in these notes start in the repo root, so that is where they appear:

```
~/Documents/selenium-practice/
    docs/
    tests/
    screenshots/      <- only after a test fails
    pytest.ini
    report.html       <- every run
    test-run.log      <- every run
```

Open them:

```
open report.html
open test-run.log
```

Each run overwrites both files, including a run of a single test.

report.html, test-run.log and screenshots/ are in .gitignore, so they stay on your machine and do not appear in git status.


IF THE TESTS FOLDER IS RENAMED

testpaths must match the real folder name. If the tests move to a folder called tests, change the line to:

```
testpaths = tests
```

Several folders, separated by spaces:

```
testpaths = tests tests
```

If testpaths does not match, a plain "python3 -m pytest" does not run the tests you expect. Naming the folder in the command still works, because a path in the command overrides testpaths.

Nothing else depends on the name FILES:

- conftest.py finds the screenshots folder from its own location (Path(__file__)).
- The Module 7 CSV file is found from the test file's location.
- Imports like "from mod5_pages import LoginPage" work in any folder, because pytest adds the test file's folder to Python's search path.

The only other places that say tests/ are the commands in the notes. Find them with:

```
git grep -n "tests/"
```

Many Python projects call this folder tests. Renaming it (git mv FILES tests) is optional.


WHY IT MATTERS / TRAPS (READ THIS PART!)

Trap 1 - A comment at the end of a line.
pytest.ini does not allow comments after a setting on the same line. The comment is read as part of the setting and breaks it. Put each comment on its own line, starting with #.

Trap 2 - --headless in addopts.
--headless is defined in tests/conftest.py, and pytest reads pytest.ini before that file is loaded. The run stops with "unrecognized arguments: --headless". It would also hide the browser on every run. Type --headless in the command when you want it.

Trap 3 - "unrecognized arguments: --headless" with a short command.
python3 -m pytest --headless should work, because testpaths points pytest at tests/ and its conftest.py. If your pytest version still stops with this error, put tests/ in the command: python3 -m pytest tests/ --headless. That always works (Module 8, Trap 2).

Trap 4 - The file in the wrong place.
pytest looks for pytest.ini in the folder you run from and the folders above it. Inside tests/, it is found only when you run from tests/. Keep it in the repo root.

Trap 5 - Running pytest from another folder.
The report and log are created in the folder you run from. Run from inside tests/ and they land in tests/, where .gitignore does not cover them by name. Always run from the repo root.

Trap 6 - Forgetting the report is overwritten.
Running one test to check a fix replaces the full report from the last complete run. Use a different --html name in the command to keep a report.

Trap 7 - Adding a marker without registering it.
With --strict-markers, a marker used on a test but not listed under markers stops the run with an error. Add every new label to pytest.ini first.

Trap 8 - Live log on every run.
log_cli = true prints every log message on screen for every run, and the output gets very long. Add --log-cli-level=INFO to the command only when you need it.


CHECK IT WORKS

```
cd ~/Documents/selenium-practice
python3 -m pytest
```

You get one line per test, a summary at the end with the skip reason, and a line saying where report.html was saved. Then:

```
open report.html
open test-run.log
```


COMMIT

```
git add pytest.ini docs/mod9_pytest-ini.md
git commit -m "pytest.ini and notes"
git push
```