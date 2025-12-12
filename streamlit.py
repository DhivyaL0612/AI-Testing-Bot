import streamlit as st
import pandas as pd
import os
import asyncio
from evaluator import run_evaluation
from dotenv import load_dotenv

import subprocess

subprocess.run(["playwright", "install"])

os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")

st.set_page_config(page_title="Janus AI Auditor", page_icon="🛡️", layout="wide")
st.title("🛡️ Janus - The LangChain AI Auditor")
st.write("Enter the URL of a public chatbot. Janus will use a browser to interact with it "
    "and use LangChain and Gemini to audit its responses for common vulnerabilities.")

with st.form("evaluation_form"):
    app_type = st.selectbox(
        "Select the type of application to test:",
        ("Chatbot", "Web Form")
    )
    
    url = st.text_input("Chatbot URL")
    submitted  = st.form_submit_button("Start Audit")

if submitted:
    st.info("Starting evaluation... See live progress log below.")
        # Create empty containers on the page. We will fill these with
    # the live log and the final results table later.
    progress_area = st.empty()
    results_area = st.empty()

    progress_log = "" # This string will accumulate all the log messages.

    async def run_and_display():
        global progress_log
        final_report = None
        log_container.empty()
        log_text = ""

        async for update in run_evaluation(url, app_type):
            if isinstance(update, str):
                log_text += update + "\\n"
                log_container.markdown(f"```\\n{log_text}\\n```")
            elif isinstance(update, dict):
                final_report = update
        

        # --- Display the Final Report ---
        if final_report:
            st.success("🎉 Audit Complete!")

            df = pd.DataFrame.from_dict(final_report, orient= 'index')
            df = df.reset_index().rename(columns={'index': 'Test Type'})

            results_area.subheader("Final Report Card")
            results_area.dataframe(df, use_container_width=True)
        else:
            st.error("Audit failed to complete. Please check the log for errors.")

    asyncio.run(run_and_display())




