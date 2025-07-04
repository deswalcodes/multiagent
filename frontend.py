import streamlit as st
import requests

st.set_page_config(page_title="Multi-Agent Assignment", page_icon="🤖")

st.title("🤖 Multi-Agent Assignment Frontend")

query = st.text_input("Ask your question:")

agent_type = st.radio(
    "Choose the agent:",
    ("Support Agent", "Dashboard Agent")
)

if st.button("Submit") and query:
    if agent_type == "Support Agent":
        endpoint = "http://127.0.0.1:5000/support"
    else:
        endpoint = "http://127.0.0.1:5000/dashboard"

    try:
        response = requests.post(
            endpoint,
            json={"query": query}
        )
        response.raise_for_status()
        result = response.json()
        st.success("**Agent Response:**")
        st.write(result.get("response"))
    except Exception as e:
        st.error(f"Error: {e}")
