import streamlit as st
import requests

st.set_page_config(page_title="Kabitix AI", page_icon="🤖")

# Custom CSS styling to make chat bubbles look modern and professional
st.markdown("""
<style>
    /* Styling for the user message box */
    .stChatMessage[data-testid="stChatMessageUser"] {
        background-color: #1E293B !important;
        border-radius: 15px !important;
        border: 1px solid #334155 !important;
    }
    /* Styling for the AI assistant message box */
    .stChatMessage[data-testid="stChatMessageAssistant"] {
        background-color: #0F172A !important;
        border-radius: 15px !important;
        border: 1px solid #1E293B !important;
    }
</style>
""", unsafe_allow_html=True)

st.title("🚀 Kabitix AI Platform")
st.write("Welcome to your 100% free, unlimited original AI engine.")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask Kabitix anything..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Kabitix is thinking..."):
            try:
                # Stable free AI backup router layout
                payload = {
                    "contents": [{"parts": [{"text": prompt}]}]
                }
                url = "https://googleapis.com"
                res = requests.post(url, json=payload, timeout=15)
                
                # Extract clean response text layout safely
                response = res.json()["candidates"][0]["content"]["parts"][0]["text"]
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
            except Exception as e:
                st.error("Connection glitch. Please try sending your message again!")
