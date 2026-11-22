
SELENIUM WITH PYTHON - MODULE 6: TRICKY ELEMENTS
(alerts, frames, multiple windows, file uploads)


GOAL

Handle the four things that break most beginner scripts: browser alerts, content inside frames, links that open a new tab or window, and file uploads. They look different, but they share one idea.


THE ONE IDEA: SELENIUM LOOKS IN ONE PLACE AT A TIME

Selenium always works in one place: the main page, one frame, one window, or an open alert. It only sees what is in that place. If something is somewhere else, Selenium cannot find it, even when you can see it on screen.

Most errors in this module come from Selenium looking in the wrong place. The fix is always the same: switch to the right place, do the work, then switch back.

- Alert: wait with EC.alert_is_present(), then accept or dismiss
- Frame: switch into the frame, then driver.switch_to.default_content() to go back
- Window: driver.switch_to.window(handle)
- File upload is the exception: no switching, you type the file path into the input


PART 1 - JAVASCRIPT ALERTS

Browsers have three built-in dialogs, opened by the page's JavaScript:

- alert: a message with an OK button
- confirm: a question with OK and Cancel
- prompt: a question with a text box, OK and Cancel

These are not part of the page, so find_element cannot see them. Wait for the dialog, then work with it:

```python
from selenium.webdriver.support import expected_conditions as EC

alert = WebDriverWait(driver, 10).until(EC.alert_is_present())

message = alert.text        # read the message FIRST
alert.accept()              # click OK
# alert.dismiss()           # click Cancel (confirm and prompt)
# alert.send_keys("hello")  # type into a prompt, then accept()
```

EC.alert_is_present() waits for the dialog and returns it. That is the Module 2 rule again: wait for the thing, then use it.

While a dialog is open, the page is frozen. Selenium cannot click or read anything else until the dialog is accepted or dismissed.


PART 2 - IFRAMES AND FRAMES

An iframe is a separate web page embedded inside another page. Common examples: embedded editors, reports, maps, payment forms. Older sites use frames (a page split into several frames), which work the same way.

Elements inside a frame belong to the frame's own page. From the main page, Selenium cannot find them:

```python
# Main page: the element is inside a frame, so this finds nothing
driver.find_elements(By.ID, "content")      # [] (empty list)

# Switch into the frame first
WebDriverWait(driver, 10).until(
    EC.frame_to_be_available_and_switch_to_it("frame-name")
)
driver.find_element(By.ID, "content").text  # now it works

# Switch back to the main page when done
driver.switch_to.default_content()
```

Ways to point at a frame:

- By its name or id: EC.frame_to_be_available_and_switch_to_it("editor")
- By a locator: EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR, "iframe.report"))

Frames inside frames (nested): switch one level at a time, from the outside in.

- driver.switch_to.default_content() goes all the way back to the main page.
- driver.switch_to.parent_frame() goes up one level only.

How to tell if an element is inside a frame: right-click it in Chrome, choose Inspect, and look up the tree in the Elements panel. If there is an iframe (or frame) above it, you must switch first.


PART 3 - MULTIPLE TABS AND WINDOWS

Every tab or window has an ID called a window handle. Selenium stays in the window it is in, even when a click opens a new tab and the browser shows that new tab.

```python
original = driver.current_window_handle
before = set(driver.window_handles)

driver.find_element(By.LINK_TEXT, "Click Here").click()   # opens a new tab

# Wait for the new tab, then find its handle
WebDriverWait(driver, 10).until(EC.number_of_windows_to_be(len(before) + 1))
new_handle = (set(driver.window_handles) - before).pop()

driver.switch_to.window(new_handle)    # now Selenium works in the new tab
# ... work in the new tab ...

driver.close()                         # closes ONLY the current tab
driver.switch_to.window(original)      # go back - this step is required
```

- driver.window_handles is the list of all open tabs and windows.
- Subtracting the "before" set finds the one handle that is new.
- driver.close() closes the current tab. driver.quit() closes everything and ends the session (the fixture does this).


PART 4 - FILE UPLOADS

Clicking a file input opens the operating system's file picker. Selenium only controls the browser, not that picker, so never click the input. Instead, type the file's full path into the input:

```python
file_input = driver.find_element(By.ID, "file-upload")
file_input.send_keys("/full/path/to/file.txt")   # must be a full (absolute) path
driver.find_element(By.ID, "file-submit").click()
```

The file must really exist on the machine where the browser runs.

In tests, create the file on the fly with pytest's built-in tmp_path fixture. Every test that asks for tmp_path gets a new, empty temporary folder:

```python
def test_upload_file(driver, tmp_path):
    test_file = tmp_path / "mod6_upload.txt"
    test_file.write_text("Hello from Selenium Module 6")
    page = UploadPage(driver).open().upload(test_file)
```

tmp_path is built into pytest, so it needs no code in conftest.py. A test can ask for several fixtures at once: here, driver and tmp_path.


THE FILES

- conftest.py - unchanged, gives each test a fresh browser
- mod5_pages.py - unchanged, Module 6 reuses its BasePage
- mod6_pages.py - page objects: AlertsPage, NestedFramesPage, WindowsPage, NewWindowPage, UploadPage
- mod6_tricky_test.py - 11 tests

mod6_pages.py starts with:

```python
from mod5_pages import BasePage, BASE_URL
```

BasePage was written once in Module 5. Module 6 imports it instead of copying it, so a fix to BasePage helps every module. This import line is also why the file names use underscores.

All switching happens inside the page objects. Tests never call switch_to. Each page method switches where it needs to, does the work, and switches back, so the next step always starts in a known place.


WHY IT MATTERS / TRAPS (READ THIS PART!)

Trap 1 - Reading the alert text after accepting it.
After accept() or dismiss(), the dialog is gone. Reading alert.text then raises NoAlertPresentException. Always read the text first.

Trap 2 - Doing anything else while an alert is open.
Any other command (find, click, get) raises UnexpectedAlertPresentException. Handle the dialog first.

Trap 3 - Not every popup is an alert.
Most modern apps draw their own dialogs with normal HTML (a div styled as a box). EC.alert_is_present() times out on those, because they are not browser dialogs. They are normal elements: find them and click them like anything else. If you can Inspect a popup in Chrome, it is HTML. A real browser alert cannot be inspected.

Trap 4 - Looking for an element inside a frame without switching.
You can see it on screen, but find_element raises NoSuchElementException (or a wait times out). Check with Inspect whether an iframe is above it in the tree.

Trap 5 - Forgetting to switch back.
After working in a frame, Selenium stays there. The next search for a main page element fails. Switch back with default_content(), ideally in a finally block so it happens even when something fails. NestedFramesPage does exactly that.

Trap 6 - Jumping straight into a nested frame.
You cannot jump from the main page directly into an inner frame. Switch into the outer frame first, then the inner one.

Trap 7 - Assuming Selenium follows a new tab.
A link opens a new tab and the browser shows it, but Selenium is still in the old tab. You must call switch_to.window() yourself.

Trap 8 - driver.close() without switching.
close() closes the current tab, and Selenium is left pointing at a tab that no longer exists. The next command raises NoSuchWindowException until you switch to an open window.

Trap 9 - Trusting the order of window_handles.
The order of the handles list is not guaranteed. Code like driver.window_handles[1] can switch to the wrong tab. Compare the handles before and after the click, as in Part 3.

Trap 10 - Clicking the file input.
It opens the operating system's file picker, which Selenium cannot control, and the test hangs or fails. Send the path with send_keys instead.

Trap 11 - Relative or hard-coded file paths.
A relative path like "test.txt" usually fails, because the browser needs a full path. A hard-coded path like /Users/yourname/Desktop/test.txt only works on your machine, and it puts your username in a public repo. Use tmp_path.

Trap 12 - Passing a Path object to send_keys.
tmp_path gives a Path object, not text, and send_keys expects text. Convert it with str(test_file). In this module, UploadPage.upload() does the conversion, so tests can pass either.


HANDS-ON PRACTICE

All pages are on the public practice site the-internet.herokuapp.com:

- /javascript_alerts - alert, confirm and prompt buttons
- /nested_frames - frames inside frames (LEFT, MIDDLE, RIGHT, BOTTOM)
- /windows - a link that opens a new tab
- /upload - a file upload form

Run only the Module 6 tests:

```
python3 -m pytest tests/mod6_tricky_test.py -v
```

Run one part at a time with -k (it matches part of the test name):

```
python3 -m pytest tests/mod6_tricky_test.py -v -k alert
python3 -m pytest tests/mod6_tricky_test.py -v -k frame
python3 -m pytest tests/mod6_tricky_test.py -v -k window
python3 -m pytest tests/mod6_tricky_test.py -v -k upload
```

Run everything (Modules 4, 5 and 6, 18 tests):

```
python3 -m pytest tests/ -v
```

Break it on purpose (this step is MEANT to fail):

1. In mod6_pages.py, find accept_alert() and swap these two lines, so the dialog is accepted before its text is read:
   text = alert.text
   alert.accept()
2. Run:
   python3 -m pytest tests/mod6_tricky_test.py -v -k alert_is_accepted
3. The test fails with NoAlertPresentException, and the traceback points at the alert.text line in mod6_pages.py. That is Trap 1.
4. Swap the lines back and run again. It passes.


MENTAL MODEL

Before every step, ask: where is Selenium looking right now?

- An alert is open -> handle it first, nothing else works.
- The element is inside a frame -> switch in, do the work, switch back.
- A click opened a new tab -> switch to it, and switch back after closing it.
- A file needs uploading -> send_keys the full path, never click the input.


FOR YOUR OWN APP LATER

- Internal apps often embed reports, editors or document viewers in iframes. If an element "cannot be found" but you can see it, check for an iframe first.
- Single sign-on logins sometimes open in a popup window or a new tab. The window switching from Part 3 applies.
- Export or "open in new tab" buttons create a new window handle.
- Import screens (for example, uploading a CSV file) use the same send_keys pattern. Create the test file with tmp_path, so no real data is used.
- Confirmation popups such as "Are you sure you want to delete?" are usually HTML dialogs (Trap 3), not browser alerts. Inspect before choosing an approach.


git add docs/mod6_tricky-elements.md src/selenium_practice/pages/mod6_pages.py tests/mod6_tricky_test.py
git commit -m "Module 6: alerts, frames, windows, file uploads"
git push

QUIZ (answers below - try before peeking)

1. You click a button, a browser alert appears, and your next find_element call raises UnexpectedAlertPresentException. Why, and what do you do?

2. What is wrong with this code?
   ```python
   alert = WebDriverWait(driver, 10).until(EC.alert_is_present())
   alert.accept()
   print(alert.text)
   ```

3. You can see a Save button on screen. Inspect shows it inside an iframe with id="editor". find_element times out. What do you do?

4. After reading some text inside a frame, your test can no longer find the main page's Logout link. What did you forget?

5. You click "Open report", a new tab opens and you can see the report, but driver.title still returns the old page's title. Why?

6. What is the difference between driver.close() and driver.quit()? What happens if you call find_element right after close() without switching?

7. An "Are you sure?" popup appears, but EC.alert_is_present() times out. What is the most likely reason, and how do you handle the popup?

8. DevOps stretch question: an upload test uses the path /Users/yourname/Desktop/test.txt. It passes on your Mac but fails on GitHub Actions. Why, and how does tmp_path fix it? (Just guess.)


ANSWERS

1. While a browser dialog is open, the page is frozen and Selenium cannot do anything else. Wait for it with EC.alert_is_present(), then accept() or dismiss() it before the next step.

2. The text is read after the dialog has been closed, so alert.text raises NoAlertPresentException. Read the text first, then accept.

3. Switch into the frame first, for example WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it("editor")), then find the button. Switch back with default_content() afterwards.

4. To switch back to the main page with driver.switch_to.default_content(). Selenium was still inside the frame.

5. Selenium is still in the original tab. A new tab does not move Selenium. Switch to the new window handle first.

6. close() closes only the current tab or window. quit() closes everything and ends the browser session. After close(), Selenium points at a tab that no longer exists, so find_element raises NoSuchWindowException until you switch to an open window.

7. It is probably an HTML dialog drawn by the page, not a browser alert. Treat it as normal elements: find its buttons with locators (Inspect will show them) and click.

8. The GitHub Actions runner is a different machine (usually Linux). That folder and file do not exist there, so the upload fails. tmp_path creates a new temporary folder on whatever machine runs the test, so the test creates its own file wherever it runs. It also keeps your username out of a public repo.


End of Module 6. Next up: Module 7, data-driven tests (run the same test with many different inputs using pytest parametrize).