
import streamlit as st
import requests

st.set_page_config(page_title="Kabitix AI", page_icon="🤖")
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
                # Direct unrestricted free public AI connection node
                url = f"https://pollinations.ai{requests.utils.quote(prompt)}"
                res = requests.get(url)
                response = res.text
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
            except Exception as e:
                st.error("Connection glitch. Please try sending your message again!")
