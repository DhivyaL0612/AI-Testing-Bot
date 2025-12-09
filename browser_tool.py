#This file will contain a class that can control a web browser. It will navigate to a URL, type text, and read the chatbot's response.

from playwright.async_api import async_playwright, Page, expect


class BrowserTool:
    def __init__ (self, url: str):
        self.url = url
        self.playwright = None
        self.browser = None
        self.page = None

    async def start_browser (self):
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(headless=True)
        self.page = await self.browser.new_page()
        await self.page.goto(self.url)
    

    async def send_and_get_response (self, prompt: str):
        chat_input = self.page.get_by_placeholder("Message ITTicketResolver...")
        await chat_input.fill(prompt)
        await chat_input.press("Enter")

            # Step 2: Locate where the response will appear.
        # Streamlit marks its chat message elements with a 'data-testid'.
        # We specify that we only want messages from the 'assistant' and we
        # want the '.last' one on the page, which will be the newest response.
        response_locator = self.page.locator('[data-testid="stChatMessage"]').filter(has_text="assistant").last

        # Step 3: Wait for the bot to finish "typing".
        # This is the most important step for reliability. Streamlit shows a "..."
        # while the bot is generating a response. We use 'expect' to wait until
        # that "..." is no longer visible, with a generous timeout of 60 seconds.
        await expect(response_locator.get_by_text("...").first).to_have_count(0, timeout=60000)

        # Step 4: Extract the final text from the response bubble.
        response_text = await response_locator.inner_text()

        # Step 5: Clean up the text, as it often includes the role label "assistant".
        return response_text.replace("assistant\n", "").strip()

    async def close_browser(self):
        """A cleanup function to gracefully close the browser and all its processes."""
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()
