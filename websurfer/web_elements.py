from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class WebSurfer:
    def __init__(self, headless = False):
        """
        Initialize the WebSurfer instance.

        Args:
            headless (bool, optional): Run the browser in headless mode. Defaults to False.
        """

        options = Options()
        options.headless = headless
        self.driver = webdriver.Firefox(options=options)

    def go_to(self, url):
        """
        Navigate to the given URL.

        Args:
            url (str): URL to navigate to

        Returns:
            None
        """

        self.driver.get(url)
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

    def get_text_by_selector(self, selector, by=By.CSS_SELECTOR):
        """
        Get the text content of the element matching the given selector.

        Args:
            selector (str): CSS selector or XPath expression to match
            by (By, optional): Method to use for matching. Defaults to By.CSS_SELECTOR.

        Returns:
            str: Text content of the matched element or an error message if no element is found
        """
        try:
            element = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((by, selector)))
            return element.text
        except Exception as e:
            return f"Error: {str(e)}"

    def click_element(self, selector, by=By.CSS_SELECTOR):
        """
        Click on the element matching the given selector.

        Args:
            selector (str): CSS selector or XPath expression to match.
            by (By, optional): Method to use for matching. Defaults to By.CSS_SELECTOR.

        Returns:
            str: Confirmation message if successful or an error message if the element is not clickable.
        """

        try:
            element = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((by, selector)))
            element.click()
            return "Clicked."
        except Exception as e:
            return f"Error: {str(e)}"

    def quit(self):
        """
        Quit the WebDriver instance.

        Returns:
            None
        """
        self.driver.quit()

# agent_commands = [
#     {"action": "go_to", "url": "https://news.ycombinator.com"},
#     {"action": "get_text_by_selector", "selector": "a.storylink"},
#     {"action": "click_element", "selector": "a.morelink"},
# ]

# surfer = WebSurfer()

# for cmd in agent_commands:
#     action = cmd["action"]
#     if action == "go_to":
#         surfer.go_to(cmd["url"])
#     elif action == "get_text_by_selector":
#         print(">>>>>")
#         print(surfer.get_text_by_selector(cmd["selector"]))
#     elif action == "click_element":
#         print(">>>>>")
#         print(surfer.click_element(cmd["selector"]))

# surfer.quit()
