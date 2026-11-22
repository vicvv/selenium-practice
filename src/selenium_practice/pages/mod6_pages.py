"""
mod6_pages.py
Selenium Module 6: page objects for alerts, frames, windows and file uploads,
using the public practice site the-internet.herokuapp.com.

BasePage and BASE_URL come from Module 5 (mod5_pages.py), so that file must
be in the same folder. All switching (alerts, frames, windows) happens inside
these classes. Tests never call switch_to.
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from selenium_practice.pages.mod5_pages import BasePage, BASE_URL


class AlertsPage(BasePage):
    URL = f"{BASE_URL}/javascript_alerts"

    ALERT_BUTTON = (By.CSS_SELECTOR, "button[onclick='jsAlert()']")
    CONFIRM_BUTTON = (By.CSS_SELECTOR, "button[onclick='jsConfirm()']")
    PROMPT_BUTTON = (By.CSS_SELECTOR, "button[onclick='jsPrompt()']")
    RESULT = (By.ID, "result")

    def open(self):
        self.driver.get(self.URL)
        self.find_visible(self.ALERT_BUTTON)
        return self

    def _open_dialog(self, button):
        """Click a button and wait for the browser dialog it opens."""
        self.click(button)
        return self.wait.until(EC.alert_is_present())

    def accept_alert(self):
        """Open the JS Alert, click OK, and return the dialog's message."""
        alert = self._open_dialog(self.ALERT_BUTTON)
        text = alert.text          # read the message BEFORE closing the dialog
        alert.accept()
        return text

    def answer_confirm(self, ok):
        """Open the JS Confirm. ok=True clicks OK, ok=False clicks Cancel."""
        alert = self._open_dialog(self.CONFIRM_BUTTON)
        text = alert.text
        if ok:
            alert.accept()
        else:
            alert.dismiss()
        return text

    def answer_prompt(self, answer=None):
        """Open the JS Prompt. Type the answer and click OK,
        or click Cancel if answer is None."""
        alert = self._open_dialog(self.PROMPT_BUTTON)
        if answer is None:
            alert.dismiss()
        else:
            alert.send_keys(answer)
            alert.accept()

    def result_text(self):
        return self.find_visible(self.RESULT).text


class NestedFramesPage(BasePage):
    URL = f"{BASE_URL}/nested_frames"

    TOP_FRAME = (By.NAME, "frame-top")
    BODY = (By.TAG_NAME, "body")
    MIDDLE_CONTENT = (By.ID, "content")

    def open(self):
        self.driver.get(self.URL)
        self.wait.until(EC.presence_of_element_located(self.TOP_FRAME))
        return self

    def _text_inside(self, frame_names, locator):
        """Switch into each frame in order (outside to inside), read the
        element's text, and always switch back to the main page."""
        self.driver.switch_to.default_content()
        try:
            for name in frame_names:
                self.wait.until(EC.frame_to_be_available_and_switch_to_it(name))
            return self.find_visible(locator).text
        finally:
            self.driver.switch_to.default_content()

    def middle_text(self):
        return self._text_inside(["frame-top", "frame-middle"], self.MIDDLE_CONTENT)

    def left_text(self):
        return self._text_inside(["frame-top", "frame-left"], self.BODY)

    def bottom_text(self):
        return self._text_inside(["frame-bottom"], self.BODY)

    def middle_found_without_switching(self):
        """True if the middle frame's content can be found from the main page.
        It cannot, because it lives inside a frame."""
        self.driver.switch_to.default_content()
        return len(self.driver.find_elements(*self.MIDDLE_CONTENT)) > 0


class WindowsPage(BasePage):
    URL = f"{BASE_URL}/windows"

    OPEN_LINK = (By.LINK_TEXT, "Click Here")
    HEADING = (By.TAG_NAME, "h3")

    def open(self):
        self.driver.get(self.URL)
        self.find_visible(self.OPEN_LINK)
        return self

    def heading_text(self):
        return self.find_visible(self.HEADING).text

    def window_count(self):
        return len(self.driver.window_handles)

    def open_new_window(self):
        """Click the link, wait for the new tab, switch to it,
        and return its page object."""
        original = self.driver.current_window_handle
        before = set(self.driver.window_handles)
        self.click(self.OPEN_LINK)
        self.wait.until(EC.number_of_windows_to_be(len(before) + 1))
        new_handle = (set(self.driver.window_handles) - before).pop()
        self.driver.switch_to.window(new_handle)
        return NewWindowPage(self.driver, return_to=original)


class NewWindowPage(BasePage):
    HEADING = (By.TAG_NAME, "h3")

    def __init__(self, driver, return_to, timeout=10):
        super().__init__(driver, timeout)
        self.return_to = return_to   # handle of the window to go back to

    def heading_text(self):
        return self.find_visible(self.HEADING).text

    def window_count(self):
        return len(self.driver.window_handles)

    def close_and_return(self):
        """Close this tab and switch back to the original one."""
        self.driver.close()
        self.driver.switch_to.window(self.return_to)
        return WindowsPage(self.driver)


class UploadPage(BasePage):
    URL = f"{BASE_URL}/upload"

    FILE_INPUT = (By.ID, "file-upload")
    SUBMIT = (By.ID, "file-submit")
    HEADING = (By.TAG_NAME, "h3")
    UPLOADED_FILES = (By.ID, "uploaded-files")

    def open(self):
        self.driver.get(self.URL)
        self.wait.until(EC.presence_of_element_located(self.FILE_INPUT))
        return self

    def upload(self, file_path):
        """Upload a file. file_path must be the full path to a file that exists.
        Never click the file input: that opens the system file picker."""
        file_input = self.wait.until(EC.presence_of_element_located(self.FILE_INPUT))
        file_input.send_keys(str(file_path))   # str() also accepts a Path object
        self.click(self.SUBMIT)
        self.find_visible(self.UPLOADED_FILES)  # wait for the result page
        return self

    def heading_text(self):
        return self.find_visible(self.HEADING).text

    def uploaded_file_name(self):
        return self.find_visible(self.UPLOADED_FILES).text