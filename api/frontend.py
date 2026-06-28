import requests
import pandas as pd
import streamlit as st
import plotly.express as px
import time
import os

API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")
st.set_page_config(page_title="NYC Taxi Analytics Copilot", layout="wide")

st.title("NYC Taxi Analytics Copilot")

if 'history' not in st.session_state:
    st.session_state.history = []

question = st.text_input('Query the database in plain English:')

if st.button("Ask") and question:
    start_time = time.time()
    with st.spinner("Fetching Insights..."):
        response = requests.post(
            f"{API_URL}/ask",
            json={
                "question": question,
                "history": st.session_state.history
            }
        )
    end_time = time.time()
    response_time = end_time - start_time

    if response.ok:
        data = response.json()

        if "error" in data:
            st.error(data["error"])
            st.code(data.get("sql", ""), language="sql")
            with st.expander("SQL"):
                st.code(data.get('sql', ''), language='sql')
        else:
            summary = data.get("summary", "")
            
            sql = data.get("sql", "")
            results = data.get("results", [])
            chart = data.get("chart")

            st.subheader("Summary")
            st.write(summary)
            st.write('Response Time: ' + str(round(response_time, 2)) + ' seconds')

            #st.subheader("Generated SQL")
            #st.code(sql, language="sql")
            with st.expander("Generated SQL"):
                st.code(data.get('sql', ''), language='sql')

            if results:
                df = pd.DataFrame(results)

                st.subheader("Results")
                st.dataframe(df, use_container_width=True)

                if chart:
                    st.subheader("Chart")

                    if chart["type"] == "bar":
                        fig = px.bar(df, x=chart["x"], y=chart["y"])
                        st.plotly_chart(fig, use_container_width=True)

                    elif chart["type"] == "line":
                        fig = px.line(df, x=chart["x"], y=chart["y"])
                        st.plotly_chart(fig, use_container_width=True)

            st.session_state.history.append({
                "user": question,
                "assistant": summary
            })
    else:
        st.error(f"API Error ({response.status_code})")
        st.code(response.text)

st.sidebar.subheader("Conversation History")

if st.sidebar.button("Clear history"):
    st.session_state.history = []
    st.rerun()

for item in st.session_state.history:
    st.sidebar.markdown(f"**User:** {item['user']}")
    st.sidebar.markdown(f"**Assistant:** {item['assistant']}")
    st.sidebar.divider()