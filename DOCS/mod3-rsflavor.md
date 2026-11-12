
SELENIUM WITH PYTHON - MODULE 3: BROWSER INTERACTIONS
(ExampleApp-flavored: login + search patterns)


GOAL

Learn the core ways to interact with page elements beyond typing: clicks, clearing fields, dropdowns, checkboxes, radio buttons, and keyboard keys (like Enter to submit a search).

We practice on public sites, but the patterns are exactly what you'll use on ExampleApp dev later (log in, pick filters, run a search).


THE INTERACTION TOOLKIT

From an element you've located:

- element.click() - Click a button/link/checkbox
- element.send_keys("text") - Type into a field
- element.clear() - Empty a field before typing
- element.send_keys(Keys.RETURN) - Press Enter (submit a search/form)
- element.text - Read the visible text
- element.get_attribute("value") - Read an input's current value
- element.is_selected() - Is a checkbox/radio checked?
- element.is_enabled() - Is it clickable/active?
- element.is_displayed() - Is it visible?


TYPING INTO FIELDS (LOGIN USERNAME/PASSWORD, SEARCH BOX)

```python
from selenium.webdriver.common.by import By

user = driver.find_element(By.ID, "username")
user.clear()                  # good habit: clear first
user.send_keys("testuser")

pwd = driver.find_element(By.ID, "password")
pwd.send_keys("secret123")
```


KEYBOARD KEYS (ENTER, TAB, ETC.)

```python
from selenium.webdriver.common.keys import Keys

search = driver.find_element(By.ID, "search")
search.send_keys("palladium")
search.send_keys(Keys.RETURN)     # press Enter to run the search
# Other handy keys: Keys.TAB, Keys.ESCAPE, Keys.ENTER (same as RETURN)
```


DROPDOWN MENUS (THE SELECT CLASS)
e.g. a "Location" or "Status" filter

Selenium has a special helper for `<select>` dropdowns. Don't just click them like normal elements - wrap them in Select.

```python
from selenium.webdriver.support.ui import Select

dropdown = Select(driver.find_element(By.ID, "status-filter"))
dropdown.select_by_visible_text("In Use")   # pick by what the user sees
dropdown.select_by_value("3")               # pick by the option's value
dropdown.select_by_index(2)                 # pick by position (0-based)

# Read the current selection:
print(dropdown.first_selected_option.text)
```


CHECKBOXES AND RADIO BUTTONS
e.g. "Only Active", "Include child locations"

```python
checkbox = driver.find_element(By.ID, "only-active")
if not checkbox.is_selected():    # only click if not already checked
    checkbox.click()

# Radio buttons: just click the one you want
driver.find_element(By.CSS_SELECTOR, "input[value='barcode']").click()
```


WHY IT MATTERS / TRAPS (READ THIS PART!)

Trap 1 - `<select>` dropdowns need the Select class.
If you try to handle a real HTML `<select>` by clicking options manually, it's fragile and often fails. Use Select(...). BUT: many modern apps (React, etc.) use fake dropdowns that are really styled `<div>` and `<ul>` lists, not `<select>`. Those you handle with normal clicks + waits. ExampleApp is React (per the specs), so expect a mix - check the actual HTML before assuming. (How to check: right-click the dropdown in Chrome -> Inspect -> is the tag `<select>` or `<div>`?)

Trap 2 - Forgetting to clear() a field.
If a field already has text and you send_keys, your text gets appended, not replaced. For login fields that usually start empty it's fine; for pre-filled fields, clear() first.

Trap 3 - Blindly clicking a checkbox toggles it the wrong way.
If it's already checked and you click "to check it," you just unchecked it. Always test is_selected() first.

Trap 4 - Clicking before the element is ready.
Combine interactions with Module 2 waits: wait for element_to_be_clickable before click. On a login page, the submit button may be disabled until both fields are filled.

Trap 5 - Keys.RETURN vs clicking a submit button.
Pressing Enter in a search box usually works, but some forms only submit via the button. If Enter does nothing, locate and .click() the submit button instead.

Trap 6 - Reading a typed value.
element.text does not return what you typed into an `<input>`. Use element.get_attribute("value") to read the current contents of an input field.


MENTAL MODEL (MAPS TO ExampleApp LATER)

- Log in: send_keys username + password -> click Login
- Set a filter: Select dropdown or click a fake-dropdown option
- Toggle an option: is_selected() check, then click if needed
- Run a search: send_keys in search box -> Keys.RETURN or click
- Verify results: wait for results -> read .text / count rows


HANDS-ON PRACTICE

Save as interactions.py, venv activated:

```
python3 FILES/interactions.py
```

- Part A uses a public login form (mimics ExampleApp login).
- Part B uses a page with a real `<select>` dropdown.
- Part C uses checkboxes (with a wait-for-state fix).

```python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()

# ---------- PART A: LOGIN FLOW ----------
driver.get("https://the-internet.herokuapp.com/login")

user = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.ID, "username"))
)
user.clear()
user.send_keys("tomsmith")

pwd = driver.find_element(By.ID, "password")
pwd.send_keys("SuperSecretPassword!")
pwd.send_keys(Keys.RETURN)

flash = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.ID, "flash"))
)
print("Login result:", flash.text.split("\n")[0])

# ---------- PART B: DROPDOWN ----------
driver.get("https://the-internet.herokuapp.com/dropdown")

dropdown = Select(
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "dropdown"))
    )
)
dropdown.select_by_visible_text("Option 2")
print("Selected:", dropdown.first_selected_option.text)

# ---------- PART C: CHECKBOXES (robust + wait for state) ----------
driver.get("https://the-internet.herokuapp.com/checkboxes")

boxes = driver.find_elements(By.CSS_SELECTOR, "#checkboxes input")
for i, box in enumerate(boxes):
    if not box.is_selected():
        box.click()
    WebDriverWait(driver, 5).until(lambda d, b=box: b.is_selected())
    print(f"Checkbox {i+1} selected?", box.is_selected())

driver.quit()
```

Expected output:

```
Login result: You logged into a secure area!
Selected: Option 2
Checkbox 1 selected? True
Checkbox 2 selected? True
```


QUIZ (answers below - try before peeking)

1. You need to read back the text a user typed into a search `<input>`. Why does element.text not work, and what do you use?

2. A field already contains "old text". You run field.send_keys("new text"). What ends up in the field, and how do you get just "new text"?

3. When should you use the Select class, and when will it not work (think about ExampleApp being a React app)?

4. Write the safe way to ensure a checkbox ends up checked, without accidentally unchecking it if it's already checked.

5. Two ways to submit a login form after filling the fields - name both.

6. Before clicking a Login button that's disabled until both fields are filled, which Module 2 condition should you wait for, and why not just presence?


ANSWERS

1. element.text returns the visible text of elements like `<div>`/`<p>`, not the contents of an `<input>`. Use element.get_attribute("value") to read what's in the field.

2. "old textnew text" - send_keys appends. Call field.clear() first, then send_keys("new text").

3. Use Select for real HTML `<select>` dropdowns. It will not work on fake dropdowns built from `<div>`/`<ul>` (common in React apps like ExampleApp) - those need normal clicks + waits. Always Inspect the element to see if the tag is `<select>`.

4. ```python
   if not checkbox.is_selected():
       checkbox.click()
   ```
   (Clicking unconditionally would toggle a checked box off.)

5. (1) Press Enter in a field: field.send_keys(Keys.RETURN). (2) Locate and .click() the submit/Login button.

6. element_to_be_clickable - it waits until the button is visible and enabled. presence only confirms it exists in the DOM; a disabled button exists but can't be clicked yet.


End of Module 3 - Next up: Module 4, Assertions + pytest (turning scripts into real PASS/FAIL tests you can run in bulk)