SELENIUM WITH PYTHON - MODULE 10: RUNNING THE TESTS ON GITHUB ACTIONS


GOAL

Run the tests automatically on GitHub's computers every time you push, so nobody has to remember to run them and problems show up straight away. This module puts together what earlier modules built: headless mode and secrets in environment variables (Module 8), screenshots and reports (Module 9), and the smoke marker (pytest.ini).


WHAT GITHUB ACTIONS IS

- A workflow is a YAML file in the repo. It says when to run and what to run.
- An event starts it: a push, a pull request, or a button click.
- A job runs on a runner: a fresh virtual machine (here Ubuntu Linux) that GitHub starts for the job and deletes when the job ends.
- A job is a list of steps. A step either runs a shell command (run:) or uses a ready-made action (uses:).
- Results appear in the repo's Actions tab, and as a green check or red X next to each commit and pull request.

Every run starts on a clean machine. Nothing from your Mac is there: no venv, no packages, no environment variables, no files outside the repo. The workflow sets everything up. That is why requirements.txt, tmp_path and Path(__file__) mattered in earlier modules.


WHERE THE FILE GOES

GitHub only reads workflow files in .github/workflows/ in the repo root. The folder name must be exact, including the dot. The file name can be anything ending in .yml.

```
mkdir -p .github/workflows
```


YAML BASICS

- key: value pairs, one per line.
- Indentation shows what belongs to what. Spaces only, never tabs.
- A line starting with "- " is an item in a list.
- A | after a key starts a value of several lines.
- # starts a comment.
- ${{ ... }} is filled in by GitHub when the workflow runs, for example ${{ secrets.TEST_PASSWORD }}.


WHAT EACH PART OF THE WORKFLOW DOES

on
  push runs it on every push to main. pull_request runs it on every pull request. workflow_dispatch adds a "Run workflow" button in the Actions tab.

permissions: contents: read
  The workflow only reads the code. Giving it no more than it needs is good practice.

runs-on: ubuntu-latest
  GitHub's current Ubuntu image. It comes with Google Chrome installed, and Selenium finds the matching driver by itself, as on your Mac.

timeout-minutes: 20
  Stops a hanging job, for example one with a forgotten breakpoint(). Without it, GitHub waits up to 6 hours.

env
  Passes the repository secrets to the tests as environment variables. This does the job of export on your Mac. The test code reads os.environ as before.

Get the code (actions/checkout)
  Copies the repo onto the runner.

Set up Python (actions/setup-python)
  Installs Python. "3.x" means the newest stable version 3. cache: pip keeps downloaded packages between runs, so later runs install faster.

Install packages
  pip install -r requirements.txt installs the same packages as on your Mac. No venv is needed, because the machine is thrown away after the job. On the runner, the command is python, not python3.

Smoke tests, then All other tests
  Both use --headless, because the runner has no screen. -m smoke runs only tests marked as smoke, and -m "not smoke" runs the rest, so nothing runs twice. If a step fails, GitHub skips the steps after it unless they say otherwise. So if the smoke tests fail, the rest do not run: if the basics are broken, there is no point waiting for everything else.

Save reports and log (if: always())
  Uploads reports/ and test-run.log whether the tests passed or failed. Each pytest step creates its own dated report, so there are two reports. test-run.log is overwritten by the second step, so it only has the last step's log.

Save failure screenshots (if: failure())
  Uploads screenshots/ only if an earlier step failed. retention-days: 7 deletes the files after a week. if-no-files-found: ignore means a missing folder is not an error.

The action versions (@v4, @v5) are the ones I know of. If the Actions tab warns about an old version, check the action's page on GitHub and update the number.


SECRETS

1. On GitHub, open the repo, then Settings, then Secrets and variables, then Actions.
2. Click New repository secret. Name: TEST_USER, value: tomsmith. Save.
3. Again: name TEST_PASSWORD, value: SuperSecretPassword! Save.

The practice login is public, so this is only practice. The steps are the same for a real test account.

- Nobody can read a secret back after saving it, including you. You can only replace it.
- GitHub shows secret values in the logs as ***.
- If the secrets are not set, the Module 8 login test skips with its reason.
- Pull requests from forks (someone else's copy of the repo) do not get secrets, so that test skips there too.


SMOKE TESTS AND MARKERS

A marker is a label added with a decorator:

```python
@pytest.mark.smoke
def test_smoke_valid_login(driver):
    ...
```

- smoke is registered in pytest.ini under markers. With --strict-markers, a misspelled marker stops the run with an error.
- python3 -m pytest -m smoke runs only the marked tests. python3 -m pytest -m "not smoke" runs the rest.
- To mark a whole file, put pytestmark = pytest.mark.smoke near the top, after the imports.

Smoke tests are a small, quick set that shows whether the app is basically working: the page loads, login works.


WATCHING A RUN AND GETTING THE ARTIFACTS

- Actions tab: every run, newest first, with a green check, a red X or a yellow circle (running).
- Click a run, then the test job, then a step to see its output, the same as in your terminal.
- At the bottom of the run's summary page, under Artifacts, click one to download it as a zip.
- To start a run by hand: Actions tab, "Selenium tests" on the left, then "Run workflow".
- To rerun a failed job without a new commit: open the run and click "Re-run jobs".

In a public repo, other GitHub users can download artifacts. Never upload screenshots of a real app from a public repo.


BLOCKING MERGES WHEN TESTS FAIL (OPTIONAL)

A rule on the main branch can require the "test" check to pass before a pull request can be merged. Set it up under Settings, then Branches (or Rules). On a free GitHub account, this may only be available for public repos.


WHY IT MATTERS / TRAPS (READ THIS PART!)

Trap 1 - The workflow file in the wrong folder.
Nothing happens and there is no error. Check the path is exactly .github/workflows/ in the repo root.

Trap 2 - Tabs or wrong indentation.
The Actions tab shows "Invalid workflow file" with the line number. Use spaces only.

Trap 3 - Secret names that do not match.
secrets.TEST_PASSWORD must match the name in Settings exactly, including upper case. A missing secret is empty, so the login test skips. If a test you expected to run is SKIPPED, check the names.

Trap 4 - "It works on my Mac".
Anything not in requirements.txt, or not created by the test, is missing on the runner. After installing a package, run pip freeze > requirements.txt and commit it. Never use paths from your Mac.

Trap 5 - pip install fails on the runner.
requirements.txt was made on your Mac. If the runner rejects a pinned version, the "Install packages" step shows which one. Paste the error into the chat and we will fix it.

Trap 6 - Chrome does not start on the runner.
Errors such as "Chrome failed to start" or "DevToolsActivePort file doesn't exist". A common fix is adding --no-sandbox and --disable-dev-shm-usage to the Chrome options in conftest.py. Only add them if you see this error.

Trap 7 - Printing secrets.
GitHub masks them, but do not rely on it. Never print a password or use it in an assert.

Trap 8 - Outside sites going down.
the-internet.herokuapp.com and badssl.com are run by other people. If one is down, the run fails even though your code is fine. Use "Re-run jobs".


HANDS-ON PRACTICE

1. Check the smoke tests on your Mac:

```
python3 -m pytest -m smoke
```

   Expect 2 passed. The other tests are listed as deselected.

2. Run everything on your Mac:

```
python3 -m pytest
```

   Expect 33 passed and 1 skipped (34 passed if TEST_USER and TEST_PASSWORD are set in your terminal).

3. Add the two secrets on GitHub (see SECRETS).

4. Commit and push:

```
git pull
git add .github/workflows/mod10_selenium-tests.yml FILES/mod10_smoke_test.py DOCS/mod10_github-actions.md
git commit -m "Module 10: run tests on GitHub Actions"
git push
```

5. Open the repo on GitHub, then the Actions tab. A run starts within a few seconds. Click it and watch the steps. Expect a green check after a few minutes. Download the test-reports artifact and open a report.

Break it on purpose (this step is MEANT to fail):

1. In FILES/mod10_smoke_test.py, line 21, change
   assert "/login" in login_page.url
   to
   assert "/welcome" in login_page.url
   To confirm the line number: grep -n '"/login"' FILES/mod10_smoke_test.py
2. Commit and push.
3. In the Actions tab, the run gets a red X. The "Smoke tests" step failed, and "All other tests" was skipped.
4. Download the failure-screenshots artifact. It shows the login page, so the page loaded and only the expected text was wrong.
5. Change line 21 back, commit and push. The next run is green again.


MENTAL MODEL

- Push: GitHub starts a clean machine and runs the workflow.
- The workflow installs everything from the repo, runs smoke tests first, then the rest, headless.
- Secrets come from Settings, as environment variables.
- Evidence comes back as artifacts.
- Green check: safe. Red X: look at the step output and the artifacts.


FOR YOUR OWN APP LATER

- GitHub's runners are on the internet, so they cannot reach a site that is only on your company network. Testing an internal app from CI needs a runner inside the network (a self-hosted runner) or a pipeline your company already runs. Ask your team what is available.
- Keep tests of a real app in a private repo, so artifacts and logs are not public.
- Start with a few smoke tests on every push, and run the full set less often.


QUIZ (answers below - try before peeking)

1. You push the workflow file, but nothing appears in the Actions tab. What is the most likely cause?

2. Why does the workflow use --headless?

3. The Module 8 login test shows SKIPPED on GitHub, but you added the secrets. What should you check?

4. Why is there no "source venv/bin/activate" step in the workflow?

5. The smoke tests fail. What happens to the "All other tests" step, and why is that useful?

6. What is the difference between if: always() and if: failure()?

7. DevOps stretch question: your company's dev site is only reachable on the company network. Can GitHub's runners test it? What are the options?


ANSWERS

1. The file is not in .github/workflows/ in the repo root (wrong folder or a typo in the folder name). GitHub ignores workflow files anywhere else, without an error.

2. The runner has no screen, so Chrome cannot open a window. Without --headless, the browser fails to start.

3. That the secret names in Settings match the names in the workflow exactly (TEST_USER, TEST_PASSWORD), including upper case. Also check the run was not started by a pull request from a fork, because those do not get secrets.

4. The runner is a fresh machine used for one job and then deleted, so there is nothing to keep separate. Packages are installed straight onto it with pip install -r requirements.txt.

5. It is skipped, because a failed step stops the steps after it unless they use if:. If the basics are broken, running everything else would only waste time and produce more failures with the same cause.

6. if: always() runs the step whether the earlier steps passed or failed (used for reports). if: failure() runs it only if an earlier step failed (used for screenshots).

7. No, GitHub's hosted runners are on the public internet and cannot reach the company network. Options: a self-hosted runner installed on a machine inside the network, or the company's own CI system. Either way, check with the system owners first.


End of Module 10 - the end of the course. 