import streamlit as st
from groq import Groq

# Main configurations
st.title("Kabitix AI Platform")
st.write("Welcome to the unlimited, original Kabitix AI.")

# Read your key safely from the Streamlit Secrets vault
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# Manage chat history state
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
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama3-8b-8192",
        )
        response = chat_completion.choices.message.content
        st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})
