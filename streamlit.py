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
    url = st.text_input("Application URL", "https://cipherbot-c876c3efdmtjuepftzaejw.streamlit.app/")
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

        async for update in run_evaluation(url):
            if isinstance(update, str):
                log_text += update + "\n"
                log_container.markdown(f"```\n{log_text}\n```")
            elif isinstance(update, dict):
                final_report = update
        
        # At the end of the process, return the final result.
        return final_report
    
    # Run the async function and capture its return value.
    # This is the standard way to get a result from an asyncio.run() call.
    final_report_from_async = asyncio.run(run_and_display())
    
    # --- Display the Final Report ---
    if final_report_from_async:
        st.success("🎉 Audit Complete!")
        st.subheader("Final Report Card 📊")
        report_df = pd.DataFrame.from_dict(final_report_from_async, orient='index')
        st.table(report_df)
    else:
        st.error("Audit failed to produce a final report. Please check the log for errors.")


