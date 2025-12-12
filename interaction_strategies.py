# FILE: interaction_strategies.py - THE FINAL, CORRECT VERSION

from abc import ABC, abstractmethod
from playwright.async_api import Page

class InteractionStrategy(ABC):
    """Abstract base class for all interaction strategies."""
    @abstractmethod
    async def execute_and_get_response(self, page: Page, prompt: str) -> str:
        pass

class ChatbotStrategy(InteractionStrategy):
    """Strategy for interacting with a standard chatbot interface."""
    async def execute_and_get_response(self, page: Page, prompt: str) -> str:
        # THE FIX: We use the most specific and reliable selector for Streamlit apps
        # and ensure we are calling methods on it correctly.
        chat_input = page.locator('textarea[data-testid="stChatInput"]')
        
        await chat_input.fill(prompt)
        await chat_input.press("Enter")
        
        # Wait for the chatbot to finish responding. This selector waits for the
        # *last* chat message on the page to contain a rendered paragraph,
        # which indicates the streaming is complete.
        await page.wait_for_selector(
            '[data-testid="stChatMessage"]:last-child [data-testid="stMarkdownContainer"] p',
            state='attached',
            timeout=60000
        )
        
        # Get the text of the very last chat message element.
        response_element = page.locator('[data-testid="stChatMessage"]').last()
        return await response_element.inner_text()

class WebFormStrategy(InteractionStrategy):
    """Strategy for interacting with the Ciphor Bot's web form."""
    async def execute_and_get_response(self, page: Page, prompt: str) -> str:
        # Locate form elements by their labels and roles.
        topic_input = page.get_by_label("Main topic of your research:")
        questions_input = page.get_by_label("Specific questions or subtopics you are interested in exploring:")
        submit_button = page.get_by_role("button", name="Start Research 🚀")

        # Fill the form fields.
        await topic_input.fill(prompt)
        await questions_input.fill("Please elaborate on the main topic.")
        
        # Click submit and wait for the results.
        await submit_button.click()
        
        # Wait for the results header to appear.
        result_header_selector = "h2:has-text('Results of your research project')"
        await page.wait_for_selector(result_header_selector, timeout=120000) # 2 minute timeout
        
        # Scrape the result text.
        result_container = page.locator(f"{result_header_selector} + div")
        return await result_container.inner_text()
