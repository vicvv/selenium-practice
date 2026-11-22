"""
mod6_tricky_test.py
Selenium Module 6: tests for alerts, frames, windows and file uploads.
No locators and no switch_to calls here - they live in mod6_pages.py.

Run from the repo root with the venv active:
    python3 -m pytest FILES/mod6_tricky_test.py -v
"""

from selenium_practice.pages.mod6_pages import AlertsPage, NestedFramesPage, WindowsPage, UploadPage


# ---------- ALERTS ----------

def test_alert_is_accepted(driver):
    page = AlertsPage(driver).open()
    message = page.accept_alert()
    assert "I am a JS Alert" in message
    assert "You successfully clicked an alert" in page.result_text()


def test_alert_confirm_ok(driver):
    page = AlertsPage(driver).open()
    page.answer_confirm(ok=True)
    assert "You clicked: Ok" in page.result_text()


def test_alert_confirm_cancel(driver):
    page = AlertsPage(driver).open()
    page.answer_confirm(ok=False)
    assert "You clicked: Cancel" in page.result_text()


def test_alert_prompt_typed_text(driver):
    page = AlertsPage(driver).open()
    page.answer_prompt("hello selenium")
    assert "You entered: hello selenium" in page.result_text()


def test_alert_prompt_cancel(driver):
    page = AlertsPage(driver).open()
    page.answer_prompt(None)
    assert "You entered: null" in page.result_text()


# ---------- FRAMES ----------

def test_frame_middle_text(driver):
    page = NestedFramesPage(driver).open()
    assert "MIDDLE" in page.middle_text()


def test_frame_left_and_bottom_text(driver):
    page = NestedFramesPage(driver).open()
    assert "LEFT" in page.left_text()
    assert "BOTTOM" in page.bottom_text()


def test_frame_content_hidden_from_main_page(driver):
    page = NestedFramesPage(driver).open()
    assert not page.middle_found_without_switching()


# ---------- WINDOWS ----------

def test_window_link_opens_new_tab(driver):
    new_window = WindowsPage(driver).open().open_new_window()
    assert new_window.window_count() == 2
    assert "New Window" in new_window.heading_text()


def test_window_close_and_return(driver):
    back = WindowsPage(driver).open().open_new_window().close_and_return()
    assert back.window_count() == 1
    assert "Opening a new window" in back.heading_text()


# ---------- FILE UPLOAD ----------

def test_upload_file(driver, tmp_path):
    test_file = tmp_path / "mod6_upload.txt"
    test_file.write_text("Hello from Selenium Module 6")

    page = UploadPage(driver).open().upload(test_file)

    assert "File Uploaded!" in page.heading_text()
    assert "mod6_upload.txt" in page.uploaded_file_name()