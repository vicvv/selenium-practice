================================================================
SELENIUM WITH PYTHON — MODULE 2: WAITS
================================================================

GOAL
Learn how to make Selenium wait for the page/elements to be ready
BEFORE interacting with them. This is THE fix for "flaky" tests —
tests that pass sometimes and fail other times for no clear reason.
If you only master one Selenium topic deeply, make it this one.


WHY WAITS EXIST (the core problem)
----------------------------------------------------------------
Modern web pages load in stages. The browser shows the page, THEN
JavaScript fills in content, animations finish, data arrives from
the server, buttons become clickable, etc.

Your Selenium script runs FAST — often faster than the page can
get ready. So you ask for a button that exists one moment later,
and Selenium says "not found" and crashes. The element wasn't
missing... your script was just too early.

Waits tell Selenium: "pause and keep checking until this is ready
(up to a time limit), THEN continue."


THE THREE KINDS OF WAITING
----------------------------------------------------------------
1. time.sleep(5)        -> DUMB wait. Always waits the full time.
2. Implicit wait        -> global "retry finding for up to N sec".
3. Explicit wait        -> WebDriverWait: wait for a SPECIFIC condition.
                           *** This is the one you should use. ***


1) time.sleep() — the trap
----------------------------------------------------------------
import time
time.sleep(5)   # pauses EXACTLY 5 seconds, every time, no matter what

- If the page is ready in 0.3s, you STILL waste 5 full seconds.
- If the page takes 6s, your test FAILS anyway (5 wasn't enough).
- Fine for "let me watch it with my eyes" debugging. NEVER for
  real waiting on elements. It makes tests slow AND still flaky.


2) Implicit wait — the "set once" option
----------------------------------------------------------------
driver.implicitly_wait(10)   # set ONCE, applies to ALL find_element calls

- After this, every find_element will keep retrying for up to 10s
  before giving up.
- Simple, but blunt: it only waits for elements to EXIST, not to
  be visible or clickable. And it applies globally.
- OK as a safety net, but explicit waits are more precise.


3) Explicit wait — WebDriverWait (USE THIS)
----------------------------------------------------------------
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# Wait up to 10 seconds for a SPECIFIC condition to be true:
element = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.ID, "submit-btn"))
)
element.click()

How to read that:
- WebDriverWait(driver, 10) -> "I'll wait up to 10 seconds."
- .until( ... )             -> "...checking repeatedly until..."
- EC.element_to_be_clickable((By.ID, "submit-btn"))
                           -> "...this button is clickable."
- As soon as the condition is true, it returns the element and
  moves on. If 10s pass and it's never true -> TimeoutException.

Note the DOUBLE parentheses: the locator is a TUPLE passed to the
condition -> EC.something( (By.ID, "x") ). Forgetting the inner
parentheses is a super common beginner error.


THE EXPECTED CONDITIONS YOU'LL ACTUALLY USE
----------------------------------------------------------------
EC.presence_of_element_located((By.ID, "x"))
    -> element EXISTS in the page (may be invisible). Good for
       "has the page loaded this element at all?"

EC.visibility_of_element_located((By.ID, "x"))
    -> element exists AND is visible (not hidden/zero-size).
       Good before reading text.

EC.element_to_be_clickable((By.ID, "x"))
    -> element is visible AND enabled. Use this BEFORE .click().
       The most useful one for buttons/links.

EC.text_to_be_present_in_element((By.ID, "x"), "Success")
    -> wait until specific text appears inside an element.

EC.title_is("Dashboard") / EC.title_contains("Dash")
    -> wait until the page title matches.

EC.invisibility_of_element_located((By.ID, "spinner"))
    -> wait until a loading spinner DISAPPEARS. Very handy.


WHY IT MATTERS / TRAPS (read this part!)
----------------------------------------------------------------
TRAP 1 — DON'T MIX implicit and explicit waits. Setting
implicitly_wait() AND using WebDriverWait together can cause
unpredictable, longer-than-expected wait times (they stack in
confusing ways). Pick explicit waits and leave implicit at 0.
Rule of thumb: use WebDriverWait, don't call implicitly_wait().

TRAP 2 — "found" is NOT "ready". presence_of_element_located
finds an element that EXISTS but may be invisible or disabled.
If you then .click() it, you can get an ElementNotInteractable
error. For clicking, use element_to_be_clickable. (This is the
exact cliffhanger from Module 1.)

TRAP 3 — The double-parentheses tuple. This is WRONG:
    EC.element_to_be_clickable(By.ID, "x")      # missing inner ()
This is RIGHT:
    EC.element_to_be_clickable((By.ID, "x"))    # locator is a tuple

TRAP 4 — time.sleep() feels like it "works" and that's the danger.
It passes on your fast machine today, then fails in CI or on a slow
network tomorrow. Flaky tests erode everyone's trust in the test
suite. Explicit waits adapt to actual speed: fast when the page is
fast, patient when it's slow.

TRAP 5 — A too-short timeout causes false failures. If something
legitimately takes 12s and your wait is 10s, you'll get a
TimeoutException even though the app is fine. Tune timeouts to
realistic worst-case load times (but don't set them huge "just in
case" — that hides real problems).

TRAP 6 — Waiting for the wrong condition. Waiting for presence when
you need visibility (e.g. to read .text) can return an element whose
text is still empty. Match the condition to what you're about to do.


MENTAL MODEL (keep this)
----------------------------------------------------------------
- Going to READ text?        -> visibility_of_element_located
- Going to CLICK?            -> element_to_be_clickable
- Just checking it EXISTS?   -> presence_of_element_located
- Waiting for a spinner gone -> invisibility_of_element_located


HANDS-ON PRACTICE
----------------------------------------------------------------
Save as waits.py in selenium-practice, venv activated, then run:
    python3 waits.py

This uses Selenium's official "dynamic loading" practice page,
which deliberately loads an element AFTER a delay — perfect for
seeing waits in action.

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()
driver.get("https://the-internet.herokuapp.com/dynamic_loading/1")

# 1. Click "Start" — wait until it's CLICKABLE first (good habit)
start_btn = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "#start button"))
)
start_btn.click()

# 2. A loading spinner appears, then after a few seconds the hidden
#    text "Hello World!" is revealed. Wait for it to be VISIBLE.
#    (If you tried to read it immediately, it would be empty/hidden.)
finish_text = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.ID, "finish"))
)

print("Revealed text:", finish_text.text)

# 3. Demonstrate a TIMEOUT on purpose (optional learning moment).
#    We look for something that will never appear, with a short 3s
#    limit, and catch the error instead of crashing.
from selenium.common.exceptions import TimeoutException
try:
    WebDriverWait(driver, 3).until(
        EC.presence_of_element_located((By.ID, "this-will-never-exist"))
    )
except TimeoutException:
    print("As expected: timed out waiting for a missing element.")

driver.quit()

EXPECTED OUTPUT (in your terminal):
    Revealed text: Hello World!
    As expected: timed out waiting for a missing element.

Watch the browser: you'll SEE the spinner spin for a few seconds,
then "Hello World!" appear. Your script waited exactly as long as
needed — no more, no less. That's the whole point.


QUIZ (answers at the bottom — try before peeking)
----------------------------------------------------------------
Q1. Why is time.sleep(5) considered a bad way to wait for an
    element, even though it often "works"?

Q2. You need to click a button that appears a few seconds after
    the page loads. Which expected_condition should you use, and
    why not presence_of_element_located?

Q3. What's wrong with this line, and how do you fix it?
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located(By.ID, "finish")
    )

Q4. What happens if the condition in a WebDriverWait is never met
    within the timeout? What's the exception called?

Q5. You're about to read an element's .text to check a success
    message. Should you wait for presence, visibility, or
    clickability? Why?

Q6. True or false: it's a good idea to set both
    driver.implicitly_wait(10) AND use WebDriverWait everywhere,
    for "extra safety." Explain.


ANSWERS
----------------------------------------------------------------
A1. time.sleep() always waits the FULL fixed time regardless of
    whether the element is ready. It wastes time when the page is
    fast, and still FAILS when the page is slower than the sleep.
    It's both slow and flaky. Explicit waits adapt to real speed.

A2. element_to_be_clickable. presence_of_element_located only
    confirms the element EXISTS in the DOM — it might be invisible
    or disabled, so clicking it could throw ElementNotInteractable.
    element_to_be_clickable guarantees it's visible AND enabled.

A3. The locator must be a TUPLE (double parentheses). It should be:
        EC.visibility_of_element_located((By.ID, "finish"))
    The version shown passes two separate arguments, which is wrong.

A4. It raises a TimeoutException. (From
    selenium.common.exceptions — you can catch it with try/except
    if a timeout is a valid outcome you want to handle.)

A5. visibility_of_element_located. The element must be visible for
    its text to be reliably populated and readable. Presence alone
    might return an element whose text is still empty/hidden.

A6. False. Mixing implicit and explicit waits can produce
    unpredictable, inflated wait times because they interact in
    confusing ways. Best practice: leave implicit wait at 0 and use
    explicit WebDriverWait where you need it.

================================================================
END OF MODULE 2 — Next up: Module 3, Browser Interactions
(clicks, typing, dropdowns, checkboxes, keyboard keys) + a
real multi-step form flow.
================================================================