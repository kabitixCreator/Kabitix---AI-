import streamlit as st
import requests
import urllib.parse

st.set_page_config(page_title="Kabitix AI", page_icon="🤖", layout="wide")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Sidebar
with st.sidebar:
    st.title("Kabitix AI")
    st.success("✅ Unlimited & Free")
    
    if st.button("+ New Chat", use_container_width=True):
        st.session_state.messages = []
    
    menu = st.radio("Menu", ["💬 Chat", " Images", "⚙️ Settings"])

# Main Chat Interface
if menu == "💬 Chat":
    st.title("💬 AI Chat")
    st.caption("Your 100% free, unlimited AI engine")
    
    # Show chat history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])
    
    # User input
    if prompt := st.chat_input("Ask anything..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    url = f"https://text.pollinations.ai/{urllib.parse.quote(prompt)}"
                    response = requests.get(url, timeout=10).text
                    st.write(response)
                    st.session_state.messages.append({"role": "assistant", "content": response})
                except:
                    st.write("Error! Try again.")
                    st.session_state.messages.append({"role": "assistant", "content": "Error! Try again."})

# Image Generator
elif menu == "🎨 Images":
    st.title("🎨 Image Generator")
    prompt = st.text_input("Describe image:")
    if st.button("Generate"):
        if prompt:
            url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote(prompt)}"
            st.image(url, caption=prompt)

# Settings
elif menu == "⚙️ Settings":
    st.title("⚙️ Settings")
    if st.button("Clear Chat History"):
        st.session_state.messages = []
        st.success("Cleared!")
