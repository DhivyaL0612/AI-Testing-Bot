# FILE: streamlit.py - THE FINAL VERSION

import streamlit as st
import pandas as pd
import os
import asyncio
from evaluator import run_evaluation
from dotenv import load_dotenv
import subprocess

subprocess.run(["playwright", "install"])
subprocess.run(["sudo", "playwright", "install-deps"]) # Add this for system dependencies

load_dotenv()
if os.getenv("GOOGLE_API_KEY"):
    os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")

st.set_page_config(page_title="Janus AI Auditor", page_icon="🛡️", layout="wide")
st.title("🛡️ Janus - The Generic AI Auditor")
st.write(
    "Enter the URL of any public Streamlit app (chatbot or form-based). "
    "Janus will automatically interact with it and audit its responses for toxicity."
)

with st.form("evaluation_form"):
    url = st.text_input("Application URL", "https://itticketresolver-r2jgwbppbsqw2fgi2aebre.streamlit.app/")
    submitted = st.form_submit_button("Start Audit 🚀")

if submitted:
    st.info("🚀 Starting evaluation... See live progress log below.")
    log_container = st.empty()

    async def run_and_display():
        log_text = ""
        final_report = None 

        async for update in run_evaluation(url):
            if isinstance(update, str):
                log_text += update + "\n"
                log_container.markdown(f"```\n{log_text}\n```")
            elif isinstance(update, dict):
                final_report = update
        return final_report
    
    final_report_from_async = asyncio.run(run_and_display())
    
    if final_report_from_async:
        st.success("🎉 Audit Complete!")
        st.subheader("Final Report Card 📊")
        report_df = pd.DataFrame.from_dict(final_report_from_async, orient='index')
        st.table(report_df)
    else:
        st.error("Audit failed to produce a final report. Please check the log for errors.")
