# FILE: streamlit.py - THE FINAL, CORRECT VERSION

import streamlit as st
import pandas as pd
import os
import asyncio
from evaluator import run_evaluation
from dotenv import load_dotenv
import subprocess

# This command runs "playwright install" on the server the first time the app starts.
subprocess.run(["playwright", "install"])

# Load environment variables
load_dotenv()
if os.getenv("GOOGLE_API_KEY"):
    os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")

# --- UI Configuration ---
st.set_page_config(page_title="Janus AI Auditor", page_icon="🛡️", layout="wide")
st.title("🛡️ Janus - The AI Application Auditor")
st.write(
    "Enter the URL of a public Streamlit app. Janus will use a browser to interact with it "
    "and use open-source tools to audit its responses for toxicity."
)

with st.form("evaluation_form"):
    app_type = st.selectbox(
        "Select the type of application to test:",
        ("Chatbot", "Web Form"),
        help="Choose 'Chatbot' for apps with a chat input. Choose 'Web Form' for apps with labeled fields and a submit button."
    )
    
    url = st.text_input("Application URL", "https://itticketresolver-r2jgwbppbsqw2fgi2aebre.streamlit.app/")
    submitted = st.form_submit_button("Start Audit 🚀")

# --- Main Logic ---
if submitted:
    st.info("🚀 Starting evaluation... See live progress log below.")
    
    log_container = st.empty()

    # This is our nested async function that will run the evaluation and update the UI.
    async def run_and_display():
        # Initialize variables *inside* this function's scope.
        log_text = ""
        final_report = None 

        async for update in run_evaluation(url, app_type):
            if isinstance(update, str):
                log_text += update + "\n"
                log_cont
