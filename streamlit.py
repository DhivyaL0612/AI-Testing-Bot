# FILE: streamlit.py - THE FINAL VERSION

import streamlit as st
import pandas as pd
import os
import asyncio
from evaluator import run_evaluation
from dotenv import load_dotenv
import subprocess

# This command runs "playwright install" on the server the first time the app starts.
# It ensures the necessary browsers are downloaded.
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
    
    # We create a container that will hold our live log updates.
    log_container = st.empty()
    final_report = None

    async def run_and_display():
        nonlocal final_report # Allows this function to modify the outer 'final_report'
        log_text = ""

        # This is the main loop that gets live updates from the evaluator.
        async for update in run_evaluation(url, app_type):
            if isinstance(update, str):
                # This is a log message. Append it and display.
                log_text += update + "\n" # <-- FIX: Corrected to single \n
                log_container.markdown(f"```\n{log_text}\n```") # <-- FIX: Using the correct variable 'log_container'
            elif isinstance(update, dict):
                # This is the final dictionary. Store it.
                final_report = update
    
    # Run the entire asynchronous process.
    asyncio.run(run_and_display())
    
    # --- Display the Final Report ---
    if final_report:
        st.success("🎉 Audit Complete!")
        st.subheader("Final Report Card 📊")
        report_df = pd.DataFrame.from_dict(final_report, orient='index')
        st.table(report_df)
    else:
        st.error("Audit failed to produce a final report. Please check the log for errors.")

