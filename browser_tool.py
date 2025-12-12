
from playwright.async_api import async_playwright, Browser, Page

class BrowserTool:
    """A simple tool to manage a Playwright browser instance."""
    def __init__(self, url: str):
        self.url = url
        self.playwright = None
        self.browser: Browser | None = None
        self.page: Page | None = None

    async def start_browser(self):
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(headless=True)
        self.page = await self.browser.new_page()
        await self.page.goto(self.url)

    async def close_browser(self):
        if self.page:
            await self.page.close()
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()
