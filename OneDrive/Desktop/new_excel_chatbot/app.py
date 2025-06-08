import os
import requests
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import re
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
API_KEY = os.getenv("GROQ_API_KEY")
API_URL = "https://api.groq.com/openai/v1/chat/completions"
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
}

# Streamlit setup
st.set_page_config(page_title="Excel Chat Assistant (Groq)", layout="wide")
st.title(" Excel Chat Assistant")

# Session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Normalize columns
def clean_column_names(df):
    df.columns = [col.strip().lower().replace(" ", "_").replace("-", "_") for col in df.columns]
    return df

# Render chart
def render_chart(df, chart_type, x, y=None):
    fig, ax = plt.subplots(figsize=(8, 4))
    if chart_type == "bar":
        if y and y in df.columns:
            sns.barplot(data=df, x=x, y=y, ax=ax)
        else:
            df[x].value_counts().plot(kind="bar", ax=ax)
    elif chart_type == "hist":
        df[x].plot(kind="hist", ax=ax)
    elif chart_type == "line":
        if y and y in df.columns:
            df.plot(x=x, y=y, kind="line", ax=ax)
    elif chart_type == "pie":
        df[x].value_counts().plot(kind="pie", autopct="%1.1f%%", ax=ax)
        ax.set_ylabel("")
    plt.xticks(rotation=45)
    st.pyplot(fig)

# Upload Excel file
uploaded_file = st.file_uploader(" Upload your Excel (.xlsx) file", type=["xlsx"])
if uploaded_file:
    df = pd.read_excel(uploaded_file)
    df = clean_column_names(df)
    st.subheader(" Data Preview")
    st.dataframe(df.head(20))
    st.markdown("** Normalized Column Names:**")
    st.code(", ".join(df.columns))

    context = df.head(100).to_csv(index=False)
    column_list = ", ".join(df.columns)

    # Chat history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input("Ask a question about your data..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Prepare LLM prompt
        llm_prompt = f"""
You are a pandas expert. The user uploaded a CSV file. A sample is below:

{context}

The normalized column names in the dataset are: {column_list}

Based on the question: "{prompt}", respond ONLY with JSON like this:

{{
  "code": "<Python code to compute the result and assign to variable `result`>",
  "chart": "<bar|line|hist|pie|none>",
  "x": "<x axis column>",
  "y": "<y axis column or empty>"
}}

Use ONLY column names from the list above. Do not assume any columns exist unless shown.
"""

        # Call Groq LLM
        payload = {
            "model": "llama3-70b-8192",
            "messages": [
                {"role": "system", "content": "You are a helpful data analyst."},
                {"role": "user", "content": llm_prompt}
            ],
            "temperature": 0.2
        }

        with st.spinner("Analyzing your question..."):
            res = requests.post(API_URL, headers=HEADERS, json=payload)
            result = res.json()
            content = result["choices"][0]["message"]["content"]

        try:
            parsed = json.loads(content)
            code = parsed["code"]
            chart = parsed.get("chart", "none")
            x = parsed.get("x", "")
            y = parsed.get("y", "")

            # Execute safely
            local_vars = {"df": df}
            exec(code, {}, local_vars)
            answer = local_vars.get("result")

            response_msg = f"**Answer:** `{answer}`"
            st.session_state.messages.append({"role": "assistant", "content": response_msg})
            with st.chat_message("assistant"):
                st.markdown(response_msg)

                if chart != "none" and x in df.columns:
                    st.markdown("####  Chart")
                    render_chart(df, chart, x, y if y in df.columns else None)

        except Exception as e:
            error_msg = f" Error: {str(e)}"
            st.session_state.messages.append({"role": "assistant", "content": error_msg})
            with st.chat_message("assistant"):
                st.error(error_msg)
else:
    st.info("Upload an Excel file to start chatting with your data.")
