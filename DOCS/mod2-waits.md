SELENIUM WITH PYTHON - MODULE 2: WAITS


GOAL

Learn how to make Selenium wait for the page/elements to be ready before interacting with them. This is the fix for "flaky" tests - tests that pass sometimes and fail other times for no clear reason. If you master one Selenium topic deeply, make it this one.


WHY WAITS EXIST (THE CORE PROBLEM)

Modern web pages load in stages. The browser shows the page, then JavaScript fills in content, animations finish, data arrives from the server, buttons become clickable, etc.

Your Selenium script runs fast - often faster than the page can get ready. So you ask for a button that exists one moment later, and Selenium says "not found" and crashes. The element wasn't missing... your script was just too early.

Waits tell Selenium: "pause and keep checking until this is ready (up to a time limit), then continue."


THE THREE KINDS OF WAITING

- time.sleep(5): Dumb wait - always waits the full time
- Implicit wait: Global "retry finding for up to N sec"
- Explicit wait (WebDriverWait): Wait for a specific condition - use this


1) time.sleep() - the trap

```python
import time
time.sleep(5)   # pauses EXACTLY 5 seconds, every time, no matter what
```

- If the page is ready in 0.3s, you still waste 5 full seconds.
- If the page takes 6s, your test fails anyway (5 wasn't enough).
- Fine for "let me watch with my eyes" debugging. Never for real waiting on elements.


2) Implicit wait - the "set once" option

```python
driver.implicitly_wait(10)   # set ONCE, applies to ALL find_element calls
```

- Every find_element retries for up to 10s before giving up.
- Simple, but blunt: only waits for elements to exist, not to be visible or clickable. Applies globally.


3) Explicit wait - WebDriverWait (use this)

```python
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

element = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.ID, "submit-btn"))
)
element.click()
```

How to read it:

- WebDriverWait(driver, 10) -> "I'll wait up to 10 seconds."
- .until( ... ) -> "...checking repeatedly until..."
- EC.element_to_be_clickable((By.ID, "submit-btn")) -> "...this button is clickable."

As soon as the condition is true, it returns the element and moves on. If 10s pass and it's never true -> TimeoutException.

Note the double parentheses: the locator is a tuple passed to the condition -> EC.something( (By.ID, "x") ). Forgetting the inner parentheses is a super common beginner error.


THE EXPECTED CONDITIONS YOU'LL ACTUALLY USE

- presence_of_element_located: Element exists (may be invisible). "Has the page loaded this at all?"
- visibility_of_element_located: Exists and visible. Good before reading text.
- element_to_be_clickable: Visible and enabled. Use before .click(). Most useful for buttons/links.
- text_to_be_present_in_element: Wait until specific text appears inside an element.
- title_is / title_contains: Wait until the page title matches.
- invisibility_of_element_located: Wait until a loading spinner disappears.


WHY IT MATTERS / TRAPS (READ THIS PART!)

Trap 1 - Don't mix implicit and explicit waits.
Setting implicitly_wait() and using WebDriverWait together can cause unpredictable, longer-than-expected waits (they stack confusingly). Use explicit waits and leave implicit at 0.

Trap 2 - "Found" is not "ready".
presence_of_element_located finds an element that exists but may be invisible/disabled. If you .click() it, you can get ElementNotInteractable. For clicking, use element_to_be_clickable. (The exact cliffhanger from Module 1.)

Trap 3 - The double-parentheses tuple.
Wrong: EC.element_to_be_clickable(By.ID, "x"). Right: EC.element_to_be_clickable((By.ID, "x")).

Trap 4 - time.sleep() feels like it "works" - that's the danger.
It passes on your fast machine today, then fails in CI or on a slow network tomorrow. Explicit waits adapt: fast when the page is fast, patient when it's slow.

Trap 5 - A too-short timeout causes false failures.
If something legitimately takes 12s and your wait is 10s, you get a TimeoutException even though the app is fine. Tune timeouts to realistic worst-case load times (but don't set them huge "just in case" - that hides real problems).

Trap 6 - Waiting for the wrong condition.
Waiting for presence when you need visibility (e.g. to read .text) can return an element whose text is still empty. Match the condition to what you're about to do.


MENTAL MODEL (KEEP THIS)

- Going to read text -> wait for visibility_of_element_located
- Going to click -> wait for element_to_be_clickable
- Just check it exists -> wait for presence_of_element_located
- Wait for a spinner gone -> wait for invisibility_of_element_located


HANDS-ON PRACTICE

Save as waits.py, venv activated, then run:

```
python3 FILES/waits.py
```

This uses Selenium's official "dynamic loading" practice page, which deliberately loads an element after a delay - perfect for seeing waits in action.

```python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

driver = webdriver.Chrome()
driver.get("https://the-internet.herokuapp.com/dynamic_loading/1")

# 1. Click "Start" — wait until it's CLICKABLE first (good habit)
start_btn = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "#start button"))
)
start_btn.click()

# 2. A spinner appears, then the hidden text "Hello World!" is revealed.
#    Wait for it to be VISIBLE (reading it immediately would be empty/hidden).
finish_text = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.ID, "finish"))
)
print("Revealed text:", finish_text.text)

# 3. Demonstrate a TIMEOUT on purpose (optional learning moment).
try:
    WebDriverWait(driver, 3).until(
        EC.presence_of_element_located((By.ID, "this-will-never-exist"))
    )
except TimeoutException:
    print("As expected: timed out waiting for a missing element.")

driver.quit()
```

Expected output:

```
Revealed text: Hello World!
As expected: timed out waiting for a missing element.
```

Watch the browser: you'll see the spinner spin for a few seconds, then "Hello World!" appear. Your script waited exactly as long as needed - no more, no less. That's the whole point.


QUIZ (answers below - try before peeking)

1. Why is time.sleep(5) a bad way to wait for an element, even though it often "works"?

2. You need to click a button that appears a few seconds after the page loads. Which expected condition should you use, and why not presence_of_element_located?

3. What's wrong with this line, and how do you fix it?
   ```python
   WebDriverWait(driver, 10).until(
       EC.visibility_of_element_located(By.ID, "finish")
   )
   ```

4. What happens if the condition in a WebDriverWait is never met within the timeout? What's the exception called?

5. You're about to read an element's .text to check a success message. Should you wait for presence, visibility, or clickability? Why?

6. True or false: it's good to set both driver.implicitly_wait(10) and use WebDriverWait everywhere for "extra safety." Explain.


ANSWERS

1. time.sleep() always waits the full fixed time regardless of readiness. It wastes time when the page is fast, and still fails when the page is slower than the sleep. It's both slow and flaky. Explicit waits adapt to real speed.

2. element_to_be_clickable. presence_of_element_located only confirms the element exists - it might be invisible/disabled, so clicking could throw ElementNotInteractable. element_to_be_clickable guarantees it's visible and enabled.

3. The locator must be a tuple (double parentheses): EC.visibility_of_element_located((By.ID, "finish")). The shown version passes two separate arguments.

4. It raises a TimeoutException (from selenium.common.exceptions). Catch it with try/except if a timeout is a valid outcome.

5. visibility_of_element_located. The element must be visible for its text to be reliably populated and readable. Presence alone might return an element whose text is still empty/hidden.

6. False. Mixing implicit and explicit waits can produce unpredictable, inflated wait times. Best practice: leave implicit wait at 0 and use explicit WebDriverWait where you need it.


End of Module 2 - Next up: Module 3, Browser Interactions.