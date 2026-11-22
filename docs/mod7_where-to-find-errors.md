WHERE TO FIND ERRORS AND HOW TO SLOW TESTS DOWN


OVERVIEW

pytest does not create a log file by default. The terminal output is the log, and pytest only prints details when something fails. A passing test just shows PASSED.

This page covers where to look when a test fails, how to save the output to a file, and how to pause a test so you can watch it.


WHEN A TEST FAILS

The details are printed in the terminal, in a FAILURES section after the list of results.

- The line starting with > shows the assert that failed.
- The lines starting with E show the expected value and the actual value.
- The short summary at the very bottom lists every failure on one line.

These options make failures easier to work with:

```
python3 -m pytest tests/ -v -x          # stop at the first failure
python3 -m pytest tests/ -v --lf        # rerun only the tests that failed last time
python3 -m pytest tests/ -v -rA         # summary line for every test, passed or failed
```


SAVING THE OUTPUT TO A FILE

To keep a record, send the output to a file as well as the screen:

```
python3 -m pytest tests/ -v 2>&1 | tee test-run.log
```

You still see everything on screen, and a copy is saved in test-run.log. Open it in VS Code afterwards.

Add it to .gitignore so it does not end up in the repo:

```
echo "test-run.log" >> .gitignore
```


WATCHING A TEST AT YOUR OWN SPEED

Put breakpoint() on its own line in a test, at the point where you want it to stop:

```python
def test_valid_login_reaches_secure_area(driver):
    secure = LoginPage(driver).open().login_as(VALID_USER, VALID_PASSWORD)
    breakpoint()          # pauses here, with the browser still open
    assert secure.is_loaded()
```

Run just that one test:

```
python3 -m pytest tests/mod5_login_test.py -v -k valid_login
```

The test pauses with the browser open, so you can look at the page or even Inspect it.

In the terminal you will see a (Pdb) prompt. Type c and press Enter to continue.

Remove the line when you are done. A forgotten breakpoint() makes the test wait forever.


COMING LATER

Module 9 covers this properly:

- saving a screenshot automatically when a test fails
- writing log messages to a file
- producing an HTML report you can open in a browser

Once tests run headless or on GitHub Actions, there is no window to watch, so those become the main way to see what happened.