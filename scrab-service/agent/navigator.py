 # Playwright logic: scroll, click, extract
from playwright.sync_api import sync_playwright, Playwright

class Navigator:
    """
    This class responsible of navigating the page.
    """
    def __init__(self, url) -> None:
        self.url = url
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch()
        self.page = None


    def take_screenshot(self) -> bytes:
        pass    