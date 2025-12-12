# FILE: interaction_strategies.py - THE FINAL, CORRECTED VERSION

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
        # This selector is robust for standard Streamlit chatbots.
        chat_input = page.locator('textarea[data-testid="stChatInput"]')
        await chat_input.fill(prompt)
        await chat_input.press("Enter")
        
        # Wait for the response to finish streaming.
        await page.wait_for_selector(
            '[data-testid="stChatMessage"]:last-child [data-testid="stMarkdownContainer"] p',
            state='attached',
            timeout=60000
        )
        
        # Get the text of the last chat message.
        response_element = page.locator('[data-testid="stChatMessage"]').last()
        return await response_element.inner_text()

class WebFormStrategy(InteractionStrategy):
    """
    Strategy for interacting with a web form.
    THIS VERSION USES THE CORRECT SYNTAX.
    """
    async def execute_and_get_response(self, page: Page, prompt: str) -> str:
        # --- THE FINAL FIX IS HERE: The parentheses on .first() are removed. ---
        
        # Find the FIRST text input element on the page. .first is a property, not a function.
        topic_input = page.locator('input[type="text"]').first
        
        # Find the FIRST text area element on the page. .first is a property, not a function.
        questions_input = page.locator('textarea').first
        
        # Find the button by its role and exact name. This is robust.
        submit_button = page.get_by_role("button", name="Start Research 🚀")
        # ----------------------------------------------------------------------

        # Fill the form fields.
        await topic_input.fill(prompt)
        await questions_input.fill("Please elaborate on the main topic.")
        
        # Click submit and wait for the results.
        await submit_button.click()
        
        # Wait for the results header to appear.
        result_header_selector = "h2:has-text('Results of your research project')"
        await page.wait_for_selector(result_header_selector, timeout=120000)
        
        # Scrape the result text.
        result_container = page.locator(f"{result_header_selector} + div")
        return await result_container.inner_text()
