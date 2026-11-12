## Selenium with Python — Module 1: Locators

## Goal

Learn how to reliably find elements on a page. Everything in Selenium is: **find an element → do something to it**. Locators are the "find" half, so this module is the foundation for everything that follows.

---

## The Core Pattern

```python
from selenium.webdriver.common.by import By

element = driver.find_element(By.ID, "username")        # finds ONE element
elements = driver.find_elements(By.CLASS_NAME, "row")  # finds a LIST
```

- `find_element` → returns the **first** match. Raises an error if none found.
- `find_elements` → returns a **list**. Returns an **empty list** if none found (no error).

---

## The Locator Strategies

| Locator | When to use | Example |
|---|---|---|
| `By.ID` | Best when present — IDs are meant to be unique | `By.ID, "search-box"` |
| `By.NAME` | Form fields with a `name` attribute | `By.NAME, "q"` |
| `By.CSS_SELECTOR` | Everyday workhorse — fast and flexible | `By.CSS_SELECTOR, "input.search"` |
| `By.XPATH` | Most powerful — use only when CSS can't | `By.XPATH, "//button[text()='Login']"` |
| `By.CLASS_NAME` | One class only (no spaces) | `By.CLASS_NAME, "btn-primary"` |
| `By.LINK_TEXT` | Click a link by exact visible text | `By.LINK_TEXT, "Sign in"` |
| `By.PARTIAL_LINK_TEXT` | Match part of a link's text | `By.PARTIAL_LINK_TEXT, "Sign"` |
| `By.TAG_NAME` | All of a tag (good with `find_elements`) | `By.TAG_NAME, "a"` |

---

## Which One Should I Use? (the practical rule)

1. **`ID`** if it exists → most stable, fastest.
2. **`CSS_SELECTOR`** for most things → covers id, class, attributes, hierarchy.
3. **`XPATH`** only when you must → e.g. "find the button that says *Delete*".

Avoid relying on `CLASS_NAME` alone or on long, brittle XPaths.

---

## CSS Selector Cheat Sheet (worth memorizing)

| Selector | Matches | Example |
|---|---|---|
| `#id-name` | element with that id | `#search-box` |
| `.class-name` | element with that class | `.btn` |
| `tag` | all of that tag | `input` |
| `tag.class` | tag with that class | `input.search` |
| `[name="q"]` | element with that attribute | `[type="submit"]` |
| `parent > child` | direct child | `form > input` |
| `ancestor descendant` | any descendant | `form input` |

---

## Why It Matters / Traps (read this part!)

- **Trap 1 — `find_element` vs `find_elements` on no match.** `find_element` **raises** `NoSuchElementException` (crashes your script). `find_elements` returns an **empty list** (no crash). To check "does this exist?", use `find_elements` and test `len(results) > 0`.

- **Trap 2 — `CLASS_NAME` accepts a single class only.** If an element has `class="btn btn-primary"`, then `By.CLASS_NAME, "btn btn-primary"` **fails** (the space is invalid). Use CSS instead: `.btn.btn-primary` (join classes with dots, no spaces).

- **Trap 3 — Don't confuse argument styles.** It's `find_element(By.ID, "x")` (two arguments), **not** `find_element(By.ID("x"))` — `By.ID` is not a function.

- **Trap 4 — Fragile locators are the #1 cause of flaky tests.** Auto-generated ids like `ext-gen-1472` or deep XPaths like `/html/body/div[2]/div/div[3]/button` break the moment the page changes. Prefer stable, meaningful locators (a real id, a name, a `data-*` attribute, or text).

- **Trap 5 — `find_element` finds the first match only.** If three buttons share a class, you'll always get the first. Use `find_elements` + index, or make the locator more specific.

- **Trap 6 — Found ≠ interactable.** An element can exist in the page but still be invisible or not yet clickable. That's what `WebDriverWait` (Module 2) solves. "Found" and "ready" are not the same thing.

---

## Hands-On Practice

Save as `locators.py`, venv activated, then run:

```
python3 FILES/mod1-locators.py
```

```python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

driver = webdriver.Chrome()
driver.get("https://www.selenium.dev/selenium/web/web-form.html")

# 1. By NAME (a text input named "my-text")
text_box = driver.find_element(By.NAME, "my-text")
text_box.send_keys("hello locators")

# 2. By CSS_SELECTOR (the password field)
pwd = driver.find_element(By.CSS_SELECTOR, "input[name='my-password']")
pwd.send_keys("secret123")

# 3. By find_elements (count all the input fields on the page)
inputs = driver.find_elements(By.TAG_NAME, "input")
print("Number of <input> elements found:", len(inputs))

# 4. Safe existence check using find_elements (no crash if missing)
maybe = driver.find_elements(By.ID, "does-not-exist")
print("Did we find the fake element?", len(maybe) > 0)   # prints False

# 5. By XPATH using visible text (the Submit button)
submit = driver.find_element(By.XPATH, "//button[text()='Submit']")

time.sleep(3)   # pause so you can SEE the filled form (debug only!)
submit.click()  # submits the form -> page changes

# After submit, read the confirmation message
msg = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "message"))
)
print("Confirmation text:", msg.text)

time.sleep(3)
driver.quit()
```

**Expected output:**

```
Number of <input> elements found: (some number, e.g. 7)
Did we find the fake element? False
Confirmation text: Received!
```

---

## Quiz
*(answers below — try before peeking)*

1. You want to check whether an element exists without your script crashing. Do you use `find_element` or `find_elements`, and why?
2. An element has `class="btn btn-primary active"`. Why does `By.CLASS_NAME, "btn btn-primary"` fail, and what CSS selector matches it?
3. Write a CSS selector for: an `<input>` whose `type` attribute is `"email"`.
4. You need to click the button whose visible text is `"Delete"`. CSS can't select by text — write the XPath.
5. True or false: if `find_element` returns an element, you can always immediately `.click()` it safely. Explain.
6. Which is the most stable locator and why: (a) `By.XPATH, "/html/body/div[2]/div/div[3]/button"` (b) `By.ID, "submit-btn"` (c) `By.CLASS_NAME, "ext-gen-1472"`

---

## Answers

1. `find_elements`. It returns an empty list when nothing matches, so you can safely test `len(results) > 0`. `find_element` would raise `NoSuchElementException` and crash.
2. `By.CLASS_NAME` accepts only a **single** class; the space makes it invalid. Correct CSS: `.btn.btn-primary` (dots joining classes, no spaces). Add `.active` → `.btn.btn-primary.active`.
3. `input[type="email"]`
4. `//button[text()='Delete']` (or more forgiving of whitespace: `//button[contains(text(),'Delete')]`)
5. **False.** `find_element` only confirms the element **exists** in the DOM. It may be invisible, disabled, or not yet clickable. Use `WebDriverWait` with `element_to_be_clickable` (Module 2) before clicking.
6. **(b)** `By.ID, "submit-btn"`. IDs are meant to be unique and are usually stable/meaningful. (a) is a brittle absolute path that breaks on any layout change. (c) is an auto-generated class that changes between builds.

---

