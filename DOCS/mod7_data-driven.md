SELENIUM WITH PYTHON - MODULE 7: DATA-DRIVEN TESTS


GOAL

Run the same test many times with different inputs, without copying the test. You write the steps once and list the inputs and expected results separately. pytest turns each set of inputs into its own test, with its own result.


THE PROBLEM

In Module 5 you wrote two tests that were almost the same:

```python
def test_wrong_password_shows_error(driver):
    login_page = LoginPage(driver).open()
    login_page.login("tomsmith", "wrong-password")
    assert "Your password is invalid!" in login_page.flash_text()

def test_unknown_username_shows_error(driver):
    login_page = LoginPage(driver).open()
    login_page.login("nobody", "SuperSecretPassword!")
    assert "Your username is invalid!" in login_page.flash_text()
```

Only the data is different. Ten wrong-login cases would mean ten copies of the same steps, and a change to the steps would mean ten fixes.


PARAMETRIZE: ONE TEST, MANY INPUTS

```python
import pytest

@pytest.mark.parametrize(
    "username, password, expected",
    [
        ("tomsmith", "wrong-password", "Your password is invalid!"),
        ("nobody", "SuperSecretPassword!", "Your username is invalid!"),
    ],
)
def test_failed_login_shows_error(driver, username, password, expected):
    login_page = LoginPage(driver).open()
    login_page.login(username, password)
    assert expected in login_page.flash_text()
```

How to read it:

- The first argument is a string with the parameter names, separated by commas.
- The second argument is a list. Each item is one test case: a tuple with one value per name, in the same order.
- The test function takes parameters with exactly those names. pytest fills them in for each case.
- The test can still ask for fixtures (driver) next to the data parameters.

pytest runs the function once per case. Each case is a separate test: it gets its own fresh browser from the fixture, and it passes or fails on its own.


GIVING EACH CASE A READABLE NAME

Without names, pytest builds a name from the values, which gets long and hard to read:

```
test_failed_login_shows_error[tomsmith-wrong-password-Your password is invalid!]
```

Use pytest.param with an id:

```python
@pytest.mark.parametrize(
    "username, password, expected",
    [
        pytest.param("tomsmith", "wrong-password", "Your password is invalid!", id="wrong-password"),
        pytest.param("nobody", "SuperSecretPassword!", "Your username is invalid!", id="unknown-user"),
    ],
)
```

Now the output reads:

```
test_failed_login_shows_error[wrong-password] PASSED
test_failed_login_shows_error[unknown-user] PASSED
```

A failure report tells you straight away which case broke. You can also run only some cases with -k, because -k matches the ids too:

```
python3 -m pytest FILES/mod7_login_data_test.py -v -k empty
```


KEEPING THE DATA IN A FILE

When the list of cases grows, or when someone who does not write Python should be able to add cases, keep the data in a CSV file and load it:

```
case,username,password,expected
wrong-password,tomsmith,wrong-password,Your password is invalid!
empty-password,tomsmith,,Your password is invalid!
```

- The first row holds the column names.
- Two commas in a row (,,) mean an empty value. Empty values are useful test cases too.

Loading it in the test file:

```python
import csv
from pathlib import Path

DATA_FILE = Path(__file__).parent / "mod7_login_cases.csv"

def load_login_cases():
    with open(DATA_FILE, newline="") as f:
        return [
            pytest.param(row["username"], row["password"], row["expected"], id=row["case"])
            for row in csv.DictReader(f)
        ]

@pytest.mark.parametrize("username, password, expected", load_login_cases())
def test_failed_login_from_csv(driver, username, password, expected):
    ...
```

- csv.DictReader reads each row as a dictionary, so row["username"] gives the value in the username column.
- Path(__file__).parent is the folder the test file is in (Module 6, question 8). The data file is found on any machine that has the repo.
- newline="" is what Python's csv documentation recommends when opening a CSV file.
- The "case" column becomes the id, so the CSV file controls the test names too.


STACKING PARAMETRIZE (A PREVIEW)

Two parametrize decorators on one test run every combination:

```python
@pytest.mark.parametrize("browser_width", [800, 1400])
@pytest.mark.parametrize("username", ["nobody", "tom", ""])
def test_something(driver, browser_width, username):
    ...
```

That is 2 x 3 = 6 tests. Useful, but with browser tests the numbers grow fast (see Trap 6). This module does not use stacking. It is here so you recognize it.


THE FILES

- conftest.py - unchanged, gives each test a fresh browser
- mod5_pages.py - unchanged, Module 7 reuses its LoginPage
- mod7_login_cases.csv - the data: 4 failed-login cases
- mod7_login_data_test.py - 2 test functions: 3 cases written inline and 4 cases from the CSV file, 7 tests in total

The data file is a CSV, not a .py file, so pytest does not collect it.


WHY IT MATTERS / TRAPS (READ THIS PART!)

Trap 1 - Names that do not match.
The names in the parametrize string must match the test function's parameters exactly. A typo ("usrname") makes pytest stop with an error saying the function uses no argument with that name. It fails loudly, which is good, but it is a common first error.

Trap 2 - Wrong number of values in a case.
If the names string has 3 names, every case needs exactly 3 values. A case with 2 values makes pytest stop with an error about the wrong number of values before any test runs.

Trap 3 - A single parameter written as a bare string.
With one parameter, the list holds plain values: @pytest.mark.parametrize("username", ["nobody", "tom"]). That works. The trap is a single string instead of a list: ["nobody"] is one case, but "nobody" on its own is treated as a list of letters, giving 6 cases: "n", "o", "b" and so on.

Trap 4 - Loading the CSV with a relative path.
open("mod7_login_cases.csv") looks in the folder you ran pytest from, not the folder the test is in. From the repo root it fails with FileNotFoundError. Build the path from Path(__file__).parent.

Trap 5 - Hidden spaces in the CSV.
"tomsmith, wrong-password" (with a space after the comma) gives the password " wrong-password", with a leading space. The test then checks something different from what you think. Do not put spaces after the commas.

Trap 6 - Too many browser tests.
Every case opens and closes a browser, which takes a few seconds. 50 cases means 50 browsers. Choose cases that each test something different (see the next section), and do not add rows just because it is easy.

Trap 7 - Real credentials in a data file.
A data file with real usernames or passwords is a secret in the repo, and in a public repo everyone can read it. Use only made-up data or public demo logins (like the practice site's tomsmith), and keep real test-account passwords out of the repo, in environment variables (Module 8).

Trap 8 - One test, many unrelated checks.
Parametrize works when every case follows the same steps and the same kind of check. If some cases need extra steps or different asserts, they belong in a separate test. Lots of "if" statements inside a parametrized test are a sign of this.


CHOOSING GOOD CASES

The same ideas as in a manual test plan:

- One valid case, so you know the happy path works (Module 5 covers it here).
- One case per different reason for failure: wrong password, unknown user.
- Empty values: empty username, empty password, both empty.
- Near misses: right password in the wrong case, part of the username.
- For number fields: values on the boundaries (lowest allowed, highest allowed, one below, one above).

Each case should catch a bug the others would not. Five cases that all test "wrong password" add time but find nothing new.


HANDS-ON PRACTICE

Run only the Module 7 tests:

```
python3 -m pytest FILES/mod7_login_data_test.py -v
```

You should see 7 tests, each named after its case:

```
FILES/mod7_login_data_test.py::test_failed_login_inline[lowercase-password] PASSED
FILES/mod7_login_data_test.py::test_failed_login_inline[partial-username] PASSED
FILES/mod7_login_data_test.py::test_failed_login_inline[both-empty] PASSED
FILES/mod7_login_data_test.py::test_failed_login_from_csv[wrong-password] PASSED
FILES/mod7_login_data_test.py::test_failed_login_from_csv[empty-password] PASSED
FILES/mod7_login_data_test.py::test_failed_login_from_csv[unknown-user] PASSED
FILES/mod7_login_data_test.py::test_failed_login_from_csv[empty-username] PASSED
```

Run everything (Modules 4 to 7, 25 tests):

```
python3 -m pytest FILES/ -v
```

Add a case without touching any Python. Add this line at the end of mod7_login_cases.csv, save, and run again:

```
spaces-only,   ,SuperSecretPassword!,Your username is invalid!
```

(The username is three spaces.) There are now 8 Module 7 tests. Keep or delete the line, as you like.

Break it on purpose (this step is MEANT to fail):

1. In mod7_login_cases.csv, change the expected message on the empty-password row from
   Your password is invalid!
   to
   Wrong password!
2. Run the Module 7 tests.
3. Only test_failed_login_from_csv[empty-password] fails. All the other cases still pass, because each case is its own test.
4. Read the E line: it shows 'Wrong password!' was not found in the real banner text.
5. Change the row back.


MENTAL MODEL

- Steps: written once, in the test function.
- Data: a list of cases, inline or in a CSV file.
- pytest: one test per case, each with its own browser and its own result.
- Adding a case: one more line of data, no new test code.


FOR YOUR OWN APP LATER

- Search screens are a good fit: one search test with many search terms and expected result counts.
- Form validation: one test with many invalid inputs and the error message each one should show.
- Your manual test plan already has this shape: steps, test data and expected result. Rows with the same steps and different data are candidates for one parametrized test.
- Use only made-up data in data files. Never copy rows from a real system.


QUIZ (answers below - try before peeking)

1. A parametrized test has 6 cases. How many browsers does it open, and how many results does pytest report?

2. What is wrong here?
   @pytest.mark.parametrize("username, password", [("nobody", "x", "extra")])

3. You wrote @pytest.mark.parametrize("username", "nobody"). How many tests does pytest create, and why?

4. Why does the test file load the CSV with Path(__file__).parent instead of open("mod7_login_cases.csv")?

5. One CSV row is "wrong-password,tomsmith, wrong-password,Your password is invalid!". The test still passes. Why is this row still a problem?

6. Why give each case an id with pytest.param?

7. DevOps stretch question: your team ends up with 200 parametrized browser tests, and a full run takes 20 minutes on every pull request. Name two ways to make the run faster. (Covered in Modules 8 and 10. Just guess.)


ANSWERS

1. 6 browsers and 6 results. Each case is a separate test with its own fresh browser from the fixture.

2. The names string has 2 names (username, password), but the case has 3 values. pytest stops with an error about the wrong number of values before running anything.

3. 6 tests. A plain string is treated as a list of its letters, so pytest makes one case per letter. Write ["nobody"] for one case.

4. A relative path is looked up from the folder you ran pytest in, not the folder of the test file, so it fails with FileNotFoundError when you run from the repo root. Path(__file__).parent always points at the test file's folder, on any machine.

5. The space after the second comma makes the password " wrong-password", not "wrong-password". It still fails to log in, so the test passes, but it is testing a different input from the one you meant. That can hide a gap in your coverage.

6. So the test names in the output are short and readable, so a failure tells you straight away which case broke, and so you can run selected cases with -k.

7. Run the tests in parallel on several workers (for example with the pytest-xdist plugin), which works because the tests are independent. Run Chrome headless, which is a little faster and needed on CI anyway. Also: remove cases that test the same thing, and run the full set less often, with a small quick set on every pull request.


End of Module 7. Next up: Module 8, headless mode and Chrome options (running without a visible browser, certificate warnings, and keeping credentials out of the code).