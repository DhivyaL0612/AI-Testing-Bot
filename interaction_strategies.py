# FILE: interaction_strategies.py - THE FINAL, UNBREAKABLE VERSION

from abc import ABC, abstractmethod
from playwright.async_api import Page, Locator

class InteractionStrategy(ABC):
    @abstractmethod
    async def execute_and_get_response(self, page: Page, prompt: str) -> str:
        pass

class GenericStreamlitStrategy(InteractionStrategy):
    """
    An intelligent strategy that can interact with EITHER a Streamlit chatbot
    OR a Streamlit web form by using official data-testid attributes.
    """
    async def execute_and_get_response(self, page: Page, prompt: str) -> str:
        # Define the official selectors for all possible Streamlit inputs
        chat_input_selector = 'textarea[data-testid="stChatInput"]'
        text_input_selector = 'input[data-testid="stTextInput"]'
        text_area_selector = 'textarea[data-testid="stTextArea"]'
        
        # First, check if a chat input exists and is visible on the page
        chat_input = page.locator(chat_input_selector)
        if await chat_input.is_visible():
            # --- CHATBOT LOGIC ---
            await chat_input.fill(prompt)
            await chat_input.press("Enter")
            await page.wait_for_selector(
                '[data-testid="stChatMessage"]:last-child [data-testid="stMarkdownContainer"] p',
                state='attached',
                timeout=60000
            )
            response_element = page.locator('[data-testid="stChatMessage"]').last()
            return await response_element.inner_text()
        else:
            # --- WEB FORM LOGIC ---
            # If no chat input, find the first available text input or text area
            first_text_input = page.locator(text_input_selector).first
            first_text_area = page.locator(text_area_selector).first

            # Fill the first available text field with our toxic prompt
            if await first_text_input.is_visible():
                await first_text_input.fill(prompt)
            elif await first_text_area.is_visible():
                await first_text_area.fill(prompt)
            else:
                raise Exception("Could not find any visible st.text_input or st.text_area on the page.")

            # If there are other fields, fill them with placeholders
            all_text_inputs = await page.locator(text_input_selector).all()
            if len(all_text_inputs) > 1:
                for i in range(1, len(all_text_inputs)):
                    await all_text_inputs[i].fill("placeholder text")
            
            all_text_areas = await page.locator(text_area_selector).all()
            if len(all_text_areas) > 1:
                for i in range(1, len(all_text_areas)):
                    await all_text_areas[i].fill("placeholder text")
            
            # Find the first button on the page and click it.
            # This is a generic way to find the submit button.
            submit_button = page.locator('button[data-testid="stButton"]').first
            await submit_button.click()
            
            # Wait for results to appear by looking for any new major content
            await page.wait_for_selector("div[data-testid='stMarkdownContainer']", state='attached', timeout=120000)
            
            # Scrape all markdown containers and return the last non-empty one
            all_markdown = await page.locator("div[data-testid='stMarkdownContainer']").all_inner_texts()
            return next((text for text in reversed(all_markdown) if text.strip()), "No result text found.")
